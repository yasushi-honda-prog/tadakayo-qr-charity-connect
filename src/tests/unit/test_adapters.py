"""Unit tests for payment provider adapters."""

import hashlib
import hmac
import json

import pytest

from app.adapters.base import CheckoutSessionInput
from app.adapters.paypay import PayPayAdapter
from app.adapters.rakuten import RakutenPayAdapter
from app.models.donation import DonationStatus, PaymentProvider


class TestPayPayAdapter:
    """Tests for PayPay adapter."""

    @pytest.fixture
    def adapter(self):
        return PayPayAdapter(webhook_secret="test_secret", production_mode=False)

    @pytest.mark.asyncio
    async def test_create_checkout_session_mock_mode(self, adapter):
        """Test creating a checkout session in mock mode (no API credentials)."""
        input = CheckoutSessionInput(
            amount=1000,
            currency="JPY",
            order_id="don_123",
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
        )
        result = await adapter.create_checkout_session(input)

        # Mock mode should use our own mock payment endpoint
        assert "/mock/payment/" in result.redirect_url
        assert result.provider_order_id.startswith("paypay_")
        assert result.expires_at is not None
        # Verify URL parameters are included and properly encoded
        assert "amount=1000" in result.redirect_url
        assert "return_url=" in result.redirect_url
        assert "cancel_url=" in result.redirect_url

    @pytest.mark.asyncio
    async def test_verify_webhook_valid(self, adapter):
        """Test webhook verification with valid signature."""
        payload = {"notification_type": "COMPLETED", "merchant_payment_id": "don_123"}
        body = json.dumps(payload).encode("utf-8")
        signature = hmac.new(b"test_secret", body, hashlib.sha256).hexdigest()

        result = await adapter.verify_webhook(
            headers={"x-paypay-signature": signature},
            body=body,
        )

        assert result.valid is True
        assert result.event == payload

    @pytest.mark.asyncio
    async def test_verify_webhook_invalid_signature(self, adapter):
        """Test webhook verification with invalid signature."""
        payload = {"notification_type": "COMPLETED"}
        body = json.dumps(payload).encode("utf-8")

        result = await adapter.verify_webhook(
            headers={"x-paypay-signature": "invalid_signature"},
            body=body,
        )

        assert result.valid is False
        assert "Invalid signature" in result.error

    @pytest.mark.asyncio
    async def test_verify_webhook_missing_signature(self, adapter):
        """Test webhook verification with missing signature."""
        body = json.dumps({"notification_type": "COMPLETED"}).encode("utf-8")

        result = await adapter.verify_webhook(headers={}, body=body)

        assert result.valid is False
        assert "Missing" in result.error

    def test_normalize_event_completed(self, adapter):
        """Test normalizing a completed event."""
        event = {
            "notification_type": "CAPTURED",
            "merchant_payment_id": "don_123",
            "payment_id": "pay_456",
        }
        normalized = adapter.normalize_event(event)

        assert normalized.status == DonationStatus.COMPLETED
        assert normalized.provider_order_id == "don_123"
        assert normalized.provider_event_id == "pay_456"

    def test_normalize_event_failed(self, adapter):
        """Test normalizing a failed event."""
        event = {
            "notification_type": "FAILED",
            "merchant_payment_id": "don_123",
            "payment_id": "pay_456",
        }
        normalized = adapter.normalize_event(event)

        assert normalized.status == DonationStatus.FAILED

    @property
    def test_provider_name(self):
        """Test provider name property."""
        adapter = PayPayAdapter()
        assert adapter.provider_name == PaymentProvider.PAYPAY


class TestRakutenPayAdapter:
    """Tests for Rakuten Pay adapter."""

    @pytest.fixture
    def adapter(self):
        return RakutenPayAdapter(webhook_secret="test_secret", sandbox=True)

    @pytest.mark.asyncio
    async def test_create_checkout_session(self, adapter):
        """Test creating a checkout session."""
        input = CheckoutSessionInput(
            amount=1000,
            currency="JPY",
            order_id="don_123",
            return_url="https://example.com/thanks",
            cancel_url="https://example.com/cancel",
        )
        result = await adapter.create_checkout_session(input)

        assert result.redirect_url.startswith("https://sandbox.checkout.rakuten.co.jp")
        assert result.provider_order_id.startswith("rakuten_")
        assert result.expires_at is not None

    @pytest.mark.asyncio
    async def test_verify_webhook_valid(self, adapter):
        """Test webhook verification with valid signature."""
        payload = {"event_type": "order.captured", "order_id": "don_123"}
        body = json.dumps(payload).encode("utf-8")
        signature = hmac.new(b"test_secret", body, hashlib.sha256).hexdigest()

        result = await adapter.verify_webhook(
            headers={"x-rakuten-signature": signature},
            body=body,
        )

        assert result.valid is True
        assert result.event == payload

    def test_normalize_event_completed(self, adapter):
        """Test normalizing a completed event."""
        event = {
            "event_type": "order.captured",
            "order_id": "don_123",
            "event_id": "evt_456",
        }
        normalized = adapter.normalize_event(event)

        assert normalized.status == DonationStatus.COMPLETED
        assert normalized.provider_order_id == "don_123"
        assert normalized.provider_event_id == "evt_456"
