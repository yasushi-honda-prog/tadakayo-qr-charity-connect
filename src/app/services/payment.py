"""Payment service for handling checkout and webhook processing."""

import uuid
from datetime import UTC, datetime

import structlog

from app.adapters.base import CheckoutSessionInput, PaymentProviderAdapter, ProviderError
from app.models.donation import (
    CheckoutRequest,
    CheckoutResponse,
    Donation,
    DonationResponse,
    DonationStatus,
    PaymentEvent,
    PaymentProvider,
)
from app.repositories.donation import DonationRepositoryBase

logger = structlog.get_logger()


class PaymentServiceError(Exception):
    """Base exception for payment service errors."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class DonationNotFoundError(PaymentServiceError):
    """Raised when donation is not found."""

    def __init__(self, donation_id: str):
        super().__init__("DONATION_NOT_FOUND", f"Donation not found: {donation_id}")


class DuplicateEventError(PaymentServiceError):
    """Raised when a webhook event is already processed."""

    def __init__(self, provider: str, event_id: str):
        super().__init__("DUPLICATE_EVENT", f"Event already processed: {provider}/{event_id}")


class InvalidSignatureError(PaymentServiceError):
    """Raised when webhook signature is invalid."""

    def __init__(self, provider: str, error: str):
        super().__init__("SIGNATURE_INVALID", f"Invalid signature for {provider}: {error}")


class PaymentService:
    """Service for handling payment operations."""

    def __init__(
        self,
        repository: DonationRepositoryBase,
        adapters: dict[PaymentProvider, PaymentProviderAdapter],
    ):
        self._repository = repository
        self._adapters = adapters

    def _get_adapter(self, provider: PaymentProvider) -> PaymentProviderAdapter:
        """Get adapter for the specified provider."""
        adapter = self._adapters.get(provider)
        if not adapter:
            raise PaymentServiceError(
                "PROVIDER_UNAVAILABLE", f"Provider not configured: {provider.value}"
            )
        return adapter

    async def create_checkout(self, request: CheckoutRequest) -> CheckoutResponse:
        """Create a checkout session and return redirect URL.

        Args:
            request: Checkout request with amount, provider, etc.

        Returns:
            CheckoutResponse with redirect URL and donation ID

        Raises:
            PaymentServiceError: If checkout creation fails
        """
        adapter = self._get_adapter(request.provider)

        # Generate donation ID
        donation_id = f"don_{uuid.uuid4().hex[:16]}"

        logger.info(
            "Creating checkout session",
            donation_id=donation_id,
            provider=request.provider.value,
            amount=request.amount,
            source=request.source,
        )

        # Create checkout session with provider
        session_input = CheckoutSessionInput(
            amount=request.amount,
            currency=request.currency,
            order_id=donation_id,
            return_url=request.return_url,
            cancel_url=request.cancel_url,
            description=f"タダカヨ支援 - {request.source}",
        )

        try:
            session_result = await adapter.create_checkout_session(session_input)
        except ProviderError as e:
            logger.error(
                "Provider error during checkout creation",
                donation_id=donation_id,
                provider=request.provider.value,
                error=str(e),
            )
            raise PaymentServiceError("PROVIDER_UNAVAILABLE", str(e)) from e

        # Create donation record
        now = datetime.now(UTC)
        donation = Donation(
            id=donation_id,
            amount=request.amount,
            currency=request.currency,
            provider=request.provider,
            status=DonationStatus.PENDING,
            source=request.source,
            provider_order_id=session_result.provider_order_id,
            idempotency_key=request.idempotency_key,
            created_at=now,
            updated_at=now,
        )

        await self._repository.create(donation)

        logger.info(
            "Checkout session created",
            donation_id=donation_id,
            provider=request.provider.value,
            provider_order_id=session_result.provider_order_id,
        )

        return CheckoutResponse(
            donation_id=donation_id,
            provider=request.provider,
            redirect_url=session_result.redirect_url,
            expires_at=session_result.expires_at,
            status=DonationStatus.PENDING,
        )

    async def get_donation(self, donation_id: str) -> DonationResponse:
        """Get donation status by ID.

        Args:
            donation_id: The donation ID

        Returns:
            DonationResponse with current status

        Raises:
            DonationNotFoundError: If donation is not found
        """
        donation = await self._repository.get_by_id(donation_id)
        if not donation:
            raise DonationNotFoundError(donation_id)

        return DonationResponse(
            donation_id=donation.id,
            status=DonationStatus(donation.status),
            amount=donation.amount,
            currency=donation.currency,
            provider=PaymentProvider(donation.provider),
            source=donation.source,
            completed_at=donation.completed_at,
        )

    async def process_webhook(
        self, provider: PaymentProvider, headers: dict[str, str], body: bytes
    ) -> None:
        """Process a webhook from a payment provider.

        Args:
            provider: The payment provider
            headers: HTTP headers from the webhook request
            body: Raw request body

        Raises:
            InvalidSignatureError: If signature verification fails
            DuplicateEventError: If event was already processed
        """
        adapter = self._get_adapter(provider)

        # Verify signature
        verification = await adapter.verify_webhook(headers, body)
        if not verification.valid:
            raise InvalidSignatureError(provider.value, verification.error or "Unknown error")

        # Normalize event
        event = verification.event
        if not event:
            raise PaymentServiceError("INVALID_PAYLOAD", "Empty event payload")

        normalized = adapter.normalize_event(event)

        logger.info(
            "Processing webhook event",
            provider=provider.value,
            provider_event_id=normalized.provider_event_id,
            provider_order_id=normalized.provider_order_id,
            status=normalized.status.value,
        )

        # Check for duplicate event
        if await self._repository.event_exists(provider, normalized.provider_event_id):
            raise DuplicateEventError(provider.value, normalized.provider_event_id)

        # Save payment event
        event_id = f"evt_{uuid.uuid4().hex[:16]}"
        payment_event = PaymentEvent(
            id=event_id,
            provider=provider,
            provider_event_id=normalized.provider_event_id,
            provider_order_id=normalized.provider_order_id,
            status=normalized.status,
            received_at=datetime.now(UTC),
            raw_payload=normalized.raw_payload,
            signature_valid=True,
        )
        await self._repository.save_payment_event(payment_event)

        # Update donation status
        donation = await self._repository.get_by_provider_order_id(
            provider, normalized.provider_order_id
        )

        if donation:
            completed_at = (
                datetime.now(UTC)
                if normalized.status == DonationStatus.COMPLETED
                else None
            )
            await self._repository.update_status(
                donation.id, normalized.status, completed_at
            )
            logger.info(
                "Donation status updated from webhook",
                donation_id=donation.id,
                old_status=donation.status,
                new_status=normalized.status.value,
            )
        else:
            logger.warning(
                "Donation not found for webhook event",
                provider=provider.value,
                provider_order_id=normalized.provider_order_id,
            )
