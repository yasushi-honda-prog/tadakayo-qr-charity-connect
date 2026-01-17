"""Donation and payment event models."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PaymentProvider(str, Enum):
    """Supported payment providers."""

    PAYPAY = "paypay"
    RAKUTEN = "rakuten"


class DonationStatus(str, Enum):
    """Donation status states."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    EXPIRED = "expired"


class QRSourceType(str, Enum):
    """QR code source types."""

    FLYER = "flyer"
    CARD = "card"
    EVENT = "event"


class Donation(BaseModel):
    """Donation record stored in Firestore."""

    model_config = {"use_enum_values": True}

    id: str = Field(..., description="Firestore document ID")
    amount: int = Field(..., ge=100, le=1000000, description="Donation amount in JPY")
    currency: str = Field(default="JPY", description="Currency code")
    provider: PaymentProvider
    status: DonationStatus = Field(default=DonationStatus.PENDING)
    source: str = Field(..., description="QR source ID (e.g., flyer_a)")
    provider_order_id: str = Field(..., description="Provider's order ID")
    provider_customer_id: str | None = Field(default=None)
    idempotency_key: str = Field(..., description="Idempotency key for session creation")
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = Field(default=None)


class PaymentEvent(BaseModel):
    """Webhook event log stored in Firestore."""

    id: str = Field(..., description="Firestore document ID")
    provider: PaymentProvider
    provider_event_id: str = Field(..., description="Provider's event ID")
    provider_order_id: str = Field(..., description="Provider's order ID")
    status: DonationStatus
    received_at: datetime
    raw_payload: dict[str, Any] = Field(..., description="Raw payload (PII masked)")
    signature_valid: bool


class QRSource(BaseModel):
    """QR code source master data."""

    id: str = Field(..., description="Source ID (e.g., flyer_a)")
    name: str = Field(..., description="Display name")
    type: QRSourceType
    active: bool = Field(default=True)
    created_at: datetime
    description: str | None = Field(default=None)


# API Request/Response schemas
class CheckoutRequest(BaseModel):
    """Request for creating a checkout session."""

    amount: int = Field(..., ge=100, le=1000000, description="Amount in JPY")
    currency: str = Field(default="JPY")
    source: str = Field(..., description="QR source ID")
    provider: PaymentProvider
    return_url: str = Field(..., description="URL to redirect after payment")
    cancel_url: str = Field(..., description="URL to redirect on cancel")
    idempotency_key: str = Field(..., description="Unique key for idempotency")


class CheckoutResponse(BaseModel):
    """Response for checkout session creation."""

    donation_id: str
    provider: PaymentProvider
    redirect_url: str
    expires_at: datetime
    status: DonationStatus


class DonationResponse(BaseModel):
    """Response for donation status query."""

    donation_id: str
    status: DonationStatus
    amount: int
    currency: str
    provider: PaymentProvider
    source: str
    completed_at: datetime | None = None
