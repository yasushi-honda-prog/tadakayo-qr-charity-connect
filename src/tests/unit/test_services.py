"""Unit tests for payment service."""

import hashlib
import hmac
import json

import pytest

from app.adapters.paypay import PayPayAdapter
from app.adapters.rakuten import RakutenPayAdapter
from app.models.donation import (
    CheckoutRequest,
    DonationStatus,
    PaymentProvider,
)
from app.repositories.donation import InMemoryDonationRepository
from app.services.payment import (
    DonationNotFoundError,
    DuplicateEventError,
    InvalidSignatureError,
    PaymentService,
)


class TestPaymentService:
    """Tests for PaymentService."""

    @pytest.fixture
    def repository(self):
        return InMemoryDonationRepository()

    @pytest.fixture
    def service(self, repository):
        adapters = {
            PaymentProvider.PAYPAY: PayPayAdapter(
                webhook_secret="test_secret", production_mode=False
            ),
            PaymentProvider.RAKUTEN: RakutenPayAdapter(
                webhook_secret="test_secret", sandbox=True
            ),
        }
        return PaymentService(repository=repository, adapters=adapters)

    @pytest.mark.asyncio
    async def test_create_checkout_paypay(self, service, repository):
        """Test creating a PayPay checkout."""
        request = CheckoutRequest(
            amount=1000,
            source="flyer_a",
            provider=PaymentProvider.PAYPAY,
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
            idempotency_key="test-key-123",
        )

        response = await service.create_checkout(request)

        assert response.donation_id.startswith("don_")
        assert response.provider == PaymentProvider.PAYPAY
        assert response.status == DonationStatus.PENDING
        # Mock mode uses our own mock payment endpoint
        assert "/mock/payment/" in response.redirect_url

        # Verify donation was saved
        donation = await repository.get_by_id(response.donation_id)
        assert donation is not None
        assert donation.amount == 1000

    @pytest.mark.asyncio
    async def test_create_checkout_rakuten(self, service, repository):
        """Test creating a Rakuten Pay checkout."""
        request = CheckoutRequest(
            amount=2000,
            source="event_b",
            provider=PaymentProvider.RAKUTEN,
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
            idempotency_key="test-key-456",
        )

        response = await service.create_checkout(request)

        assert response.donation_id.startswith("don_")
        assert response.provider == PaymentProvider.RAKUTEN
        assert "sandbox.checkout.rakuten" in response.redirect_url

    @pytest.mark.asyncio
    async def test_get_donation(self, service):
        """Test getting donation status."""
        # First create a donation
        request = CheckoutRequest(
            amount=1000,
            source="flyer_a",
            provider=PaymentProvider.PAYPAY,
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
            idempotency_key="test-key-789",
        )
        checkout_response = await service.create_checkout(request)

        # Then get it
        donation_response = await service.get_donation(checkout_response.donation_id)

        assert donation_response.donation_id == checkout_response.donation_id
        assert donation_response.amount == 1000
        assert donation_response.status == DonationStatus.PENDING

    @pytest.mark.asyncio
    async def test_get_donation_not_found(self, service):
        """Test getting a non-existent donation."""
        with pytest.raises(DonationNotFoundError):
            await service.get_donation("don_nonexistent")

    @pytest.mark.asyncio
    async def test_process_webhook_paypay(self, service, repository):
        """Test processing a PayPay webhook."""
        # Create a donation first
        request = CheckoutRequest(
            amount=1000,
            source="flyer_a",
            provider=PaymentProvider.PAYPAY,
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
            idempotency_key="test-key-webhook",
        )
        checkout_response = await service.create_checkout(request)

        # Get the provider_order_id
        donation = await repository.get_by_id(checkout_response.donation_id)

        # Simulate webhook
        payload = {
            "notification_type": "CAPTURED",
            "merchant_payment_id": donation.provider_order_id,
            "payment_id": "pay_123",
        }
        body = json.dumps(payload).encode("utf-8")
        signature = hmac.new(b"test_secret", body, hashlib.sha256).hexdigest()

        await service.process_webhook(
            provider=PaymentProvider.PAYPAY,
            headers={"x-paypay-signature": signature},
            body=body,
        )

        # Verify status was updated
        updated_donation = await repository.get_by_id(checkout_response.donation_id)
        assert updated_donation.status == DonationStatus.COMPLETED.value

    @pytest.mark.asyncio
    async def test_process_webhook_invalid_signature(self, service):
        """Test processing a webhook with invalid signature."""
        payload = {"notification_type": "CAPTURED"}
        body = json.dumps(payload).encode("utf-8")

        with pytest.raises(InvalidSignatureError):
            await service.process_webhook(
                provider=PaymentProvider.PAYPAY,
                headers={"x-paypay-signature": "invalid"},
                body=body,
            )

    @pytest.mark.asyncio
    async def test_process_webhook_duplicate_event(self, service, repository):
        """Test that duplicate events are rejected."""
        # Create a donation
        request = CheckoutRequest(
            amount=1000,
            source="flyer_a",
            provider=PaymentProvider.PAYPAY,
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
            idempotency_key="test-key-duplicate",
        )
        checkout_response = await service.create_checkout(request)
        donation = await repository.get_by_id(checkout_response.donation_id)

        # First webhook
        payload = {
            "notification_type": "CAPTURED",
            "merchant_payment_id": donation.provider_order_id,
            "payment_id": "pay_duplicate_test",
        }
        body = json.dumps(payload).encode("utf-8")
        signature = hmac.new(b"test_secret", body, hashlib.sha256).hexdigest()

        await service.process_webhook(
            provider=PaymentProvider.PAYPAY,
            headers={"x-paypay-signature": signature},
            body=body,
        )

        # Second webhook with same event should fail
        with pytest.raises(DuplicateEventError):
            await service.process_webhook(
                provider=PaymentProvider.PAYPAY,
                headers={"x-paypay-signature": signature},
                body=body,
            )
