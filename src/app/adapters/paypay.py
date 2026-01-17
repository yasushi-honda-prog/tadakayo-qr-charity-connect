"""PayPay payment provider adapter.

This is a mock implementation for development.
Replace with actual PayPay API integration when credentials are available.
"""

import hashlib
import hmac
import json
import uuid
from datetime import datetime, timedelta, timezone

import structlog

from app.adapters.base import (
    CheckoutSessionInput,
    CheckoutSessionResult,
    NormalizedEvent,
    PaymentProviderAdapter,
    ProviderError,
    WebhookVerificationResult,
)
from app.models.donation import DonationStatus, PaymentProvider

logger = structlog.get_logger()

# Mock configuration - replace with actual config when available
MOCK_PAYPAY_BASE_URL = "https://sandbox.paypay.ne.jp"
MOCK_WEBHOOK_SECRET = "mock_paypay_webhook_secret"


class PayPayAdapter(PaymentProviderAdapter):
    """PayPay payment provider adapter (mock implementation)."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        merchant_id: str | None = None,
        webhook_secret: str | None = None,
        sandbox: bool = True,
    ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._merchant_id = merchant_id
        self._webhook_secret = webhook_secret or MOCK_WEBHOOK_SECRET
        self._sandbox = sandbox
        self._base_url = MOCK_PAYPAY_BASE_URL if sandbox else "https://api.paypay.ne.jp"

    @property
    def provider_name(self) -> PaymentProvider:
        return PaymentProvider.PAYPAY

    async def create_checkout_session(
        self, input: CheckoutSessionInput
    ) -> CheckoutSessionResult:
        """Create a PayPay checkout session (mock implementation).

        In production, this will call PayPay's Create a Code API.
        """
        logger.info(
            "Creating PayPay checkout session",
            order_id=input.order_id,
            amount=input.amount,
            sandbox=self._sandbox,
        )

        # Mock implementation - generate fake redirect URL
        provider_order_id = f"paypay_{uuid.uuid4().hex[:12]}"
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        # In production, this would be the actual PayPay payment URL
        redirect_url = (
            f"{self._base_url}/checkout/{provider_order_id}"
            f"?amount={input.amount}"
            f"&return_url={input.return_url}"
        )

        logger.info(
            "PayPay checkout session created",
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
        """Verify PayPay webhook signature (mock implementation).

        PayPay uses HMAC-SHA256 for webhook signature verification.
        Header: X-PAYPAY-SIGNATURE
        """
        signature = headers.get("x-paypay-signature") or headers.get("X-PAYPAY-SIGNATURE")

        if not signature:
            return WebhookVerificationResult(
                valid=False,
                error="Missing X-PAYPAY-SIGNATURE header",
            )

        # Calculate expected signature
        expected_signature = hmac.new(
            self._webhook_secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            logger.warning("PayPay webhook signature verification failed")
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

        logger.info("PayPay webhook signature verified", event_type=event.get("notification_type"))
        return WebhookVerificationResult(valid=True, event=event)

    def normalize_event(self, event: dict) -> NormalizedEvent:
        """Normalize PayPay webhook event to common format.

        PayPay notification types:
        - AUTHORIZED: Payment authorized
        - CAPTURED: Payment captured (completed)
        - FAILED: Payment failed
        - REFUNDED: Payment refunded
        - EXPIRED: Payment expired
        """
        notification_type = event.get("notification_type", "")
        merchant_payment_id = event.get("merchant_payment_id", "")
        payment_id = event.get("payment_id", "")

        status_map = {
            "AUTHORIZED": DonationStatus.PENDING,
            "CAPTURED": DonationStatus.COMPLETED,
            "COMPLETED": DonationStatus.COMPLETED,
            "FAILED": DonationStatus.FAILED,
            "REFUNDED": DonationStatus.REFUNDED,
            "EXPIRED": DonationStatus.EXPIRED,
        }

        status = status_map.get(notification_type, DonationStatus.PENDING)

        # Mask PII from raw payload
        masked_payload = {
            k: v for k, v in event.items() if k not in ("user_info", "customer_info")
        }

        return NormalizedEvent(
            status=status,
            provider_event_id=payment_id or f"evt_{uuid.uuid4().hex[:8]}",
            provider_order_id=merchant_payment_id,
            raw_payload=masked_payload,
        )
