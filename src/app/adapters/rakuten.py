"""Rakuten Pay payment provider adapter.

This is a mock implementation for development.
Replace with actual Rakuten Pay API integration when credentials are available.
"""

import hashlib
import hmac
import json
import uuid
from datetime import UTC, datetime, timedelta

import structlog

from app.adapters.base import (
    CheckoutSessionInput,
    CheckoutSessionResult,
    NormalizedEvent,
    PaymentProviderAdapter,
    WebhookVerificationResult,
)
from app.models.donation import DonationStatus, PaymentProvider

logger = structlog.get_logger()

# Mock configuration - replace with actual config when available
MOCK_RAKUTEN_BASE_URL = "https://sandbox.checkout.rakuten.co.jp"
MOCK_WEBHOOK_SECRET = "mock_rakuten_webhook_secret"


class RakutenPayAdapter(PaymentProviderAdapter):
    """Rakuten Pay payment provider adapter (mock implementation)."""

    def __init__(
        self,
        service_id: str | None = None,
        api_key: str | None = None,
        webhook_secret: str | None = None,
        sandbox: bool = True,
    ):
        self._service_id = service_id
        self._api_key = api_key
        self._webhook_secret = webhook_secret or MOCK_WEBHOOK_SECRET
        self._sandbox = sandbox
        self._base_url = (
            MOCK_RAKUTEN_BASE_URL if sandbox else "https://checkout.rakuten.co.jp"
        )

    @property
    def provider_name(self) -> PaymentProvider:
        return PaymentProvider.RAKUTEN

    async def create_checkout_session(
        self, input: CheckoutSessionInput
    ) -> CheckoutSessionResult:
        """Create a Rakuten Pay checkout session (mock implementation).

        In production, this will call Rakuten Pay's Order API.
        """
        logger.info(
            "Creating Rakuten Pay checkout session",
            order_id=input.order_id,
            amount=input.amount,
            sandbox=self._sandbox,
        )

        # Mock implementation - generate fake redirect URL
        provider_order_id = f"rakuten_{uuid.uuid4().hex[:12]}"
        expires_at = datetime.now(UTC) + timedelta(hours=1)

        # In production, this would be the actual Rakuten Pay payment URL
        redirect_url = (
            f"{self._base_url}/payment/{provider_order_id}"
            f"?amount={input.amount}"
            f"&callback={input.return_url}"
        )

        logger.info(
            "Rakuten Pay checkout session created",
            order_id=input.order_id,
            provider_order_id=provider_order_id,
            expires_at=expires_at.isoformat(),
        )

        return CheckoutSessionResult(
            redirect_url=redirect_url,
            provider_order_id=provider_order_id,
            expires_at=expires_at,
        )

    async def verify_webhook(
        self, headers: dict[str, str], body: bytes
    ) -> WebhookVerificationResult:
        """Verify Rakuten Pay webhook signature (mock implementation).

        Rakuten Pay uses HMAC-SHA256 for webhook signature verification.
        Header: X-Rakuten-Signature
        """
        signature = (
            headers.get("x-rakuten-signature") or headers.get("X-Rakuten-Signature")
        )

        if not signature:
            return WebhookVerificationResult(
                valid=False,
                error="Missing X-Rakuten-Signature header",
            )

        # Calculate expected signature
        expected_signature = hmac.new(
            self._webhook_secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            logger.warning("Rakuten Pay webhook signature verification failed")
            return WebhookVerificationResult(
                valid=False,
                error="Invalid signature",
            )

        try:
            event = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as e:
            return WebhookVerificationResult(
                valid=False,
                error=f"Invalid JSON payload: {e}",
            )

        logger.info(
            "Rakuten Pay webhook signature verified", event_type=event.get("event_type")
        )
        return WebhookVerificationResult(valid=True, event=event)

    def normalize_event(self, event: dict) -> NormalizedEvent:
        """Normalize Rakuten Pay webhook event to common format.

        Rakuten Pay event types:
        - order.authorized: Payment authorized
        - order.captured: Payment captured (completed)
        - order.cancelled: Payment cancelled
        - order.refunded: Payment refunded
        """
        event_type = event.get("event_type", "")
        order_id = event.get("order_id", "")
        event_id = event.get("event_id", "")

        status_map = {
            "order.authorized": DonationStatus.PENDING,
            "order.captured": DonationStatus.COMPLETED,
            "order.completed": DonationStatus.COMPLETED,
            "order.cancelled": DonationStatus.FAILED,
            "order.failed": DonationStatus.FAILED,
            "order.refunded": DonationStatus.REFUNDED,
            "order.expired": DonationStatus.EXPIRED,
        }

        status = status_map.get(event_type, DonationStatus.PENDING)

        # Mask PII from raw payload
        masked_payload = {
            k: v for k, v in event.items() if k not in ("customer", "buyer_info")
        }

        return NormalizedEvent(
            status=status,
            provider_event_id=event_id or f"evt_{uuid.uuid4().hex[:8]}",
            provider_order_id=order_id,
            raw_payload=masked_payload,
        )
