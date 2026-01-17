"""Unit tests for data models."""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.models.donation import (
    CheckoutRequest,
    Donation,
    DonationStatus,
    PaymentProvider,
)


class TestCheckoutRequest:
    """Tests for CheckoutRequest model."""

    def test_valid_request(self):
        """Test creating a valid checkout request."""
        request = CheckoutRequest(
            amount=1000,
            source="flyer_a",
            provider=PaymentProvider.PAYPAY,
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
            idempotency_key="test-key-123",
        )
        assert request.amount == 1000
        assert request.currency == "JPY"
        assert request.provider == PaymentProvider.PAYPAY

    def test_amount_minimum(self):
        """Test that amount must be at least 100."""
        with pytest.raises(ValidationError) as exc_info:
            CheckoutRequest(
                amount=50,
                source="flyer_a",
                provider=PaymentProvider.PAYPAY,
                return_url="https://example.com/thanks",
                cancel_url="https://example.com/cancel",
                idempotency_key="test-key-123",
            )
        assert "amount" in str(exc_info.value)

    def test_amount_maximum(self):
        """Test that amount must be at most 1000000."""
        with pytest.raises(ValidationError) as exc_info:
            CheckoutRequest(
                amount=1000001,
                source="flyer_a",
                provider=PaymentProvider.PAYPAY,
                return_url="https://example.com/thanks",
                cancel_url="https://example.com/cancel",
                idempotency_key="test-key-123",
            )
        assert "amount" in str(exc_info.value)


class TestDonation:
    """Tests for Donation model."""

    def test_valid_donation(self):
        """Test creating a valid donation."""
        now = datetime.now(timezone.utc)
        donation = Donation(
            id="don_123",
            amount=1000,
            currency="JPY",
            provider=PaymentProvider.PAYPAY,
            status=DonationStatus.PENDING,
            source="flyer_a",
            provider_order_id="paypay_abc123",
            idempotency_key="key-123",
            created_at=now,
            updated_at=now,
        )
        assert donation.id == "don_123"
        assert donation.status == DonationStatus.PENDING.value

    def test_status_transitions(self):
        """Test valid status values."""
        for status in DonationStatus:
            now = datetime.now(timezone.utc)
            donation = Donation(
                id="don_123",
                amount=1000,
                currency="JPY",
                provider=PaymentProvider.PAYPAY,
                status=status,
                source="flyer_a",
                provider_order_id="paypay_abc123",
                idempotency_key="key-123",
                created_at=now,
                updated_at=now,
            )
            assert donation.status == status.value
