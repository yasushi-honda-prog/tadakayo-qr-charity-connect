"""Unit tests for API endpoints."""

import hashlib
import hmac
import json
import pytest
from fastapi.testclient import TestClient

from app.adapters.paypay import PayPayAdapter
from app.adapters.rakuten import RakutenPayAdapter
from app.api.donations import set_payment_service
from app.main import app
from app.models.donation import PaymentProvider
from app.repositories.donation import InMemoryDonationRepository
from app.services.payment import PaymentService


@pytest.fixture
def client():
    """Create a test client with initialized services."""
    repository = InMemoryDonationRepository()
    adapters = {
        PaymentProvider.PAYPAY: PayPayAdapter(webhook_secret="test_secret", sandbox=True),
        PaymentProvider.RAKUTEN: RakutenPayAdapter(webhook_secret="test_secret", sandbox=True),
    }
    service = PaymentService(repository=repository, adapters=adapters)
    set_payment_service(service)
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestCheckoutEndpoint:
    """Tests for checkout endpoint."""

    def test_create_checkout_success(self, client):
        """Test creating a checkout session."""
        response = client.post(
            "/api/donations/checkout",
            json={
                "amount": 1000,
                "source": "flyer_a",
                "provider": "paypay",
                "return_url": "https://example.com/thanks",
                "cancel_url": "https://example.com/cancel",
                "idempotency_key": "test-key-api",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["donation_id"].startswith("don_")
        assert data["provider"] == "paypay"
        assert data["status"] == "pending"
        assert "redirect_url" in data

    def test_create_checkout_invalid_amount(self, client):
        """Test checkout with invalid amount."""
        response = client.post(
            "/api/donations/checkout",
            json={
                "amount": 50,  # Too low
                "source": "flyer_a",
                "provider": "paypay",
                "return_url": "https://example.com/thanks",
                "cancel_url": "https://example.com/cancel",
                "idempotency_key": "test-key-invalid",
            },
        )
        assert response.status_code == 422  # Validation error

    def test_create_checkout_missing_field(self, client):
        """Test checkout with missing required field."""
        response = client.post(
            "/api/donations/checkout",
            json={
                "amount": 1000,
                # Missing source, provider, etc.
            },
        )
        assert response.status_code == 422


class TestDonationEndpoint:
    """Tests for donation status endpoint."""

    def test_get_donation_success(self, client):
        """Test getting donation status."""
        # Create a donation first
        create_response = client.post(
            "/api/donations/checkout",
            json={
                "amount": 1000,
                "source": "flyer_a",
                "provider": "paypay",
                "return_url": "https://example.com/thanks",
                "cancel_url": "https://example.com/cancel",
                "idempotency_key": "test-key-get",
            },
        )
        donation_id = create_response.json()["donation_id"]

        # Get the donation
        response = client.get(f"/api/donations/{donation_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["donation_id"] == donation_id
        assert data["amount"] == 1000
        assert data["status"] == "pending"

    def test_get_donation_not_found(self, client):
        """Test getting non-existent donation."""
        response = client.get("/api/donations/don_nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"]["error"] == "DONATION_NOT_FOUND"


class TestWebhookEndpoints:
    """Tests for webhook endpoints."""

    def test_paypay_webhook_valid(self, client):
        """Test PayPay webhook with valid signature."""
        # Create a donation first
        create_response = client.post(
            "/api/donations/checkout",
            json={
                "amount": 1000,
                "source": "flyer_a",
                "provider": "paypay",
                "return_url": "https://example.com/thanks",
                "cancel_url": "https://example.com/cancel",
                "idempotency_key": "test-key-webhook",
            },
        )
        # Note: We don't have easy access to provider_order_id here
        # so this test just verifies the endpoint accepts valid signature format

        payload = {
            "notification_type": "CAPTURED",
            "merchant_payment_id": "paypay_test123",
            "payment_id": "pay_webhook_test",
        }
        body = json.dumps(payload)
        signature = hmac.new(b"test_secret", body.encode(), hashlib.sha256).hexdigest()

        response = client.post(
            "/api/webhooks/paypay",
            content=body,
            headers={
                "Content-Type": "application/json",
                "x-paypay-signature": signature,
            },
        )
        assert response.status_code == 200

    def test_paypay_webhook_invalid_signature(self, client):
        """Test PayPay webhook with invalid signature."""
        payload = {"notification_type": "CAPTURED"}
        body = json.dumps(payload)

        response = client.post(
            "/api/webhooks/paypay",
            content=body,
            headers={
                "Content-Type": "application/json",
                "x-paypay-signature": "invalid_signature",
            },
        )
        assert response.status_code == 401

    def test_rakuten_webhook_valid(self, client):
        """Test Rakuten Pay webhook with valid signature."""
        payload = {
            "event_type": "order.captured",
            "order_id": "rakuten_test123",
            "event_id": "evt_webhook_test",
        }
        body = json.dumps(payload)
        signature = hmac.new(b"test_secret", body.encode(), hashlib.sha256).hexdigest()

        response = client.post(
            "/api/webhooks/rakuten",
            content=body,
            headers={
                "Content-Type": "application/json",
                "x-rakuten-signature": signature,
            },
        )
        assert response.status_code == 200
