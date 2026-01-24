"""PayPay payment provider adapter.

Uses the official PayPay OPA SDK for API integration.
https://github.com/paypay/paypayopa-sdk-python
"""

import contextlib
import hashlib
import hmac
import json
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import paypayopa
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

# Webhook secret for signature verification
DEFAULT_WEBHOOK_SECRET = "mock_paypay_webhook_secret"


class PayPayAdapter(PaymentProviderAdapter):
    """PayPay payment provider adapter using official SDK."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        merchant_id: str | None = None,
        webhook_secret: str | None = None,
        production_mode: bool = False,
    ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._merchant_id = merchant_id
        self._webhook_secret = webhook_secret or DEFAULT_WEBHOOK_SECRET
        self._production_mode = production_mode

        # Initialize PayPay client if credentials are provided
        self._client: paypayopa.Client | None = None
        if api_key and api_secret:
            self._client = paypayopa.Client(
                auth=(api_key, api_secret),
                production_mode=production_mode,
            )
            if merchant_id:
                self._client.set_assume_merchant(merchant_id)
            logger.info(
                "PayPay client initialized",
                production_mode=production_mode,
                has_merchant_id=bool(merchant_id),
            )

    @property
    def provider_name(self) -> PaymentProvider:
        return PaymentProvider.PAYPAY

    def _create_mock_session(self, input: CheckoutSessionInput) -> CheckoutSessionResult:
        """Create a mock checkout session for testing without API credentials."""
        provider_order_id = f"paypay_{uuid.uuid4().hex[:12]}"
        expires_at = datetime.now(UTC) + timedelta(hours=1)

        # Mock sandbox URL
        base_url = "https://sandbox.paypay.ne.jp"
        redirect_url = (
            f"{base_url}/checkout/{provider_order_id}"
            f"?amount={input.amount}"
            f"&return_url={input.return_url}"
        )

        logger.info(
            "PayPay mock checkout session created",
            order_id=input.order_id,
            provider_order_id=provider_order_id,
        )

        return CheckoutSessionResult(
            redirect_url=redirect_url,
            provider_order_id=provider_order_id,
            expires_at=expires_at,
        )

    async def create_checkout_session(
        self, input: CheckoutSessionInput
    ) -> CheckoutSessionResult:
        """Create a PayPay checkout session using the SDK.

        Calls PayPay's Create a Code API (POST /v2/codes).
        If no API credentials are configured, returns a mock response for testing.
        """
        logger.info(
            "Creating PayPay checkout session",
            order_id=input.order_id,
            amount=input.amount,
            production_mode=self._production_mode,
        )

        # Mock mode: return mock response when no credentials
        if not self._client:
            return self._create_mock_session(input)

        # Prepare request for PayPay SDK
        request = {
            "merchantPaymentId": input.order_id,
            "codeType": "ORDER_QR",
            "redirectUrl": input.return_url,
            "redirectType": "WEB_LINK",
            "amount": {
                "amount": input.amount,
                "currency": input.currency,
            },
        }

        # Add optional description
        if input.description:
            request["orderDescription"] = input.description

        try:
            response = self._client.Code.create_qr_code(request)

            # Check response status
            if response.get("resultInfo", {}).get("code") != "SUCCESS":
                error_message = response.get("resultInfo", {}).get(
                    "message", "Unknown error"
                )
                logger.error(
                    "PayPay create_qr_code failed",
                    error=error_message,
                    response=response,
                )
                raise ProviderError(
                    provider=self.provider_name,
                    message=f"Failed to create checkout session: {error_message}",
                )

            data = response.get("data", {})
            redirect_url = data.get("url")
            code_id = data.get("codeId")
            expiry_date = data.get("expiryDate")

            if not redirect_url:
                raise ProviderError(
                    provider=self.provider_name,
                    message="No redirect URL in response",
                )

            # Parse expiry date
            expires_at = datetime.now(UTC) + timedelta(hours=1)
            if expiry_date:
                with contextlib.suppress(ValueError, TypeError):
                    # PayPay returns Unix timestamp in milliseconds
                    expires_at = datetime.fromtimestamp(expiry_date / 1000, tz=UTC)

            logger.info(
                "PayPay checkout session created",
                order_id=input.order_id,
                code_id=code_id,
                expires_at=expires_at.isoformat(),
            )

            return CheckoutSessionResult(
                redirect_url=redirect_url,
                provider_order_id=code_id or input.order_id,
                expires_at=expires_at,
            )

        except Exception as e:
            logger.error("PayPay SDK error", error=str(e))
            raise ProviderError(
                provider=self.provider_name,
                message=f"PayPay API error: {e}",
            ) from e

    async def verify_webhook(
        self, headers: dict[str, str], body: bytes
    ) -> WebhookVerificationResult:
        """Verify PayPay webhook signature.

        PayPay uses HMAC-SHA256 for webhook signature verification.
        Header: X-PAYPAY-SIGNATURE
        """
        signature = headers.get("x-paypay-signature") or headers.get(
            "X-PAYPAY-SIGNATURE"
        )

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

        logger.info(
            "PayPay webhook signature verified",
            notification_type=event.get("notification_type"),
            state=event.get("state"),
        )
        return WebhookVerificationResult(valid=True, event=event)

    def normalize_event(self, event: dict[str, Any]) -> NormalizedEvent:
        """Normalize PayPay webhook event to common format.

        PayPay webhook states (Web Cashier):
        - CREATED: Payment created
        - AUTHORIZED: Payment authorized
        - COMPLETED: Payment completed
        - EXPIRED: Payment expired
        - CANCELED: Payment canceled

        Also supports legacy notification_type field for backward compatibility.
        """
        # Try state field first (Web Cashier), then notification_type (legacy)
        state = event.get("state", "") or event.get("notification_type", "")
        order_id = event.get("order_id", "") or event.get("merchant_payment_id", "")
        payment_id = event.get("payment_id", "")

        status_map = {
            # Web Cashier states
            "CREATED": DonationStatus.PENDING,
            "AUTHORIZED": DonationStatus.PENDING,
            "COMPLETED": DonationStatus.COMPLETED,
            "EXPIRED": DonationStatus.EXPIRED,
            "CANCELED": DonationStatus.FAILED,
            # Legacy notification types
            "CAPTURED": DonationStatus.COMPLETED,
            "FAILED": DonationStatus.FAILED,
            "REFUNDED": DonationStatus.REFUNDED,
        }

        status = status_map.get(state, DonationStatus.PENDING)

        # Mask PII from raw payload
        masked_payload = {
            k: v for k, v in event.items() if k not in ("user_info", "customer_info")
        }

        return NormalizedEvent(
            status=status,
            provider_event_id=payment_id or f"evt_{uuid.uuid4().hex[:8]}",
            provider_order_id=order_id,
            raw_payload=masked_payload,
        )
