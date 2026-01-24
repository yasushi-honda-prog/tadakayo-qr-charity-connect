"""Abstract base class for payment provider adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.models.donation import DonationStatus, PaymentProvider


@dataclass
class CheckoutSessionInput:
    """Input for creating a checkout session."""

    amount: int
    currency: str
    order_id: str
    return_url: str
    cancel_url: str
    description: str | None = None


@dataclass
class CheckoutSessionResult:
    """Result of checkout session creation."""

    redirect_url: str
    provider_order_id: str
    expires_at: datetime


@dataclass
class WebhookVerificationResult:
    """Result of webhook signature verification."""

    valid: bool
    event: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class NormalizedEvent:
    """Normalized webhook event across providers."""

    status: DonationStatus
    provider_event_id: str
    provider_order_id: str
    raw_payload: dict[str, Any]


class PaymentProviderAdapter(ABC):
    """Abstract base class for payment provider adapters."""

    @property
    @abstractmethod
    def provider_name(self) -> PaymentProvider:
        """Return the provider identifier."""
        ...

    @abstractmethod
    async def create_checkout_session(
        self, input: CheckoutSessionInput
    ) -> CheckoutSessionResult:
        """Create a checkout session and return redirect URL.

        Args:
            input: Checkout session parameters

        Returns:
            CheckoutSessionResult with redirect URL and provider order ID

        Raises:
            ProviderError: If the provider API call fails
        """
        ...

    @abstractmethod
    async def verify_webhook(
        self, headers: dict[str, str], body: bytes
    ) -> WebhookVerificationResult:
        """Verify webhook signature.

        Args:
            headers: HTTP headers from the webhook request
            body: Raw request body

        Returns:
            WebhookVerificationResult indicating validity
        """
        ...

    @abstractmethod
    def normalize_event(self, event: dict[str, Any]) -> NormalizedEvent:
        """Normalize provider-specific event to common format.

        Args:
            event: Raw event payload from provider

        Returns:
            NormalizedEvent with status and IDs
        """
        ...


class ProviderError(Exception):
    """Exception raised when provider API call fails."""

    def __init__(self, provider: PaymentProvider, message: str, code: str | None = None):
        self.provider = provider
        self.message = message
        self.code = code
        super().__init__(f"[{provider.value}] {message}")
