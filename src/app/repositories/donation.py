"""Donation repository for Firestore operations."""

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

import structlog
from google.cloud import firestore  # type: ignore[attr-defined]

from app.models.donation import Donation, DonationStatus, PaymentEvent, PaymentProvider

logger = structlog.get_logger()


class DonationRepositoryBase(ABC):
    """Abstract base class for donation repository."""

    @abstractmethod
    async def create(self, donation: Donation) -> Donation:
        """Create a new donation record."""
        ...

    @abstractmethod
    async def get_by_id(self, donation_id: str) -> Donation | None:
        """Get donation by ID."""
        ...

    @abstractmethod
    async def get_by_provider_order_id(
        self, provider: PaymentProvider, provider_order_id: str
    ) -> Donation | None:
        """Get donation by provider order ID."""
        ...

    @abstractmethod
    async def update_status(
        self, donation_id: str, status: DonationStatus, completed_at: datetime | None = None
    ) -> Donation | None:
        """Update donation status."""
        ...

    @abstractmethod
    async def save_payment_event(self, event: PaymentEvent) -> PaymentEvent:
        """Save a payment webhook event."""
        ...

    @abstractmethod
    async def event_exists(self, provider: PaymentProvider, provider_event_id: str) -> bool:
        """Check if a payment event already exists (for idempotency)."""
        ...


class FirestoreDonationRepository(DonationRepositoryBase):
    """Firestore implementation of donation repository."""

    def __init__(self, project_id: str | None = None):
        self._db = firestore.Client(project=project_id)
        self._donations_collection = "donations"
        self._events_collection = "payment_events"

    def _donation_to_dict(self, donation: Donation) -> dict[str, Any]:
        """Convert Donation model to Firestore document."""
        return {
            "amount": donation.amount,
            "currency": donation.currency,
            "provider": donation.provider,
            "status": donation.status,
            "source": donation.source,
            "providerOrderId": donation.provider_order_id,
            "providerCustomerId": donation.provider_customer_id,
            "idempotencyKey": donation.idempotency_key,
            "createdAt": donation.created_at,
            "updatedAt": donation.updated_at,
            "completedAt": donation.completed_at,
        }

    def _dict_to_donation(self, doc_id: str, data: dict[str, Any]) -> Donation:
        """Convert Firestore document to Donation model."""
        return Donation(
            id=doc_id,
            amount=data["amount"],
            currency=data["currency"],
            provider=data["provider"],
            status=data["status"],
            source=data["source"],
            provider_order_id=data["providerOrderId"],
            provider_customer_id=data.get("providerCustomerId"),
            idempotency_key=data["idempotencyKey"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"],
            completed_at=data.get("completedAt"),
        )

    async def create(self, donation: Donation) -> Donation:
        """Create a new donation record in Firestore."""
        doc_ref = self._db.collection(self._donations_collection).document(donation.id)
        doc_ref.set(self._donation_to_dict(donation))

        logger.info(
            "Donation created",
            donation_id=donation.id,
            provider=donation.provider,
            amount=donation.amount,
        )
        return donation

    async def get_by_id(self, donation_id: str) -> Donation | None:
        """Get donation by ID from Firestore."""
        doc_ref = self._db.collection(self._donations_collection).document(donation_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        return self._dict_to_donation(doc.id, doc.to_dict())

    async def get_by_provider_order_id(
        self, provider: PaymentProvider, provider_order_id: str
    ) -> Donation | None:
        """Get donation by provider order ID."""
        provider_val = provider.value if isinstance(provider, PaymentProvider) else provider
        query = (
            self._db.collection(self._donations_collection)
            .where("provider", "==", provider_val)
            .where("providerOrderId", "==", provider_order_id)
            .limit(1)
        )

        docs = list(query.stream())
        if not docs:
            return None

        doc = docs[0]
        return self._dict_to_donation(doc.id, doc.to_dict())

    async def update_status(
        self, donation_id: str, status: DonationStatus, completed_at: datetime | None = None
    ) -> Donation | None:
        """Update donation status in Firestore."""
        doc_ref = self._db.collection(self._donations_collection).document(donation_id)

        update_data: dict[str, Any] = {
            "status": status.value if isinstance(status, DonationStatus) else status,
            "updatedAt": datetime.now(UTC),
        }

        if completed_at:
            update_data["completedAt"] = completed_at

        doc_ref.update(update_data)

        logger.info(
            "Donation status updated",
            donation_id=donation_id,
            status=status,
        )

        return await self.get_by_id(donation_id)

    async def save_payment_event(self, event: PaymentEvent) -> PaymentEvent:
        """Save a payment webhook event to Firestore."""
        provider_val = (
            event.provider.value if isinstance(event.provider, PaymentProvider)
            else event.provider
        )
        status_val = (
            event.status.value if isinstance(event.status, DonationStatus)
            else event.status
        )
        doc_ref = self._db.collection(self._events_collection).document(event.id)
        doc_ref.set({
            "provider": provider_val,
            "providerEventId": event.provider_event_id,
            "providerOrderId": event.provider_order_id,
            "status": status_val,
            "receivedAt": event.received_at,
            "rawPayload": event.raw_payload,
            "signatureValid": event.signature_valid,
        })

        logger.info(
            "Payment event saved",
            event_id=event.id,
            provider=event.provider,
            provider_event_id=event.provider_event_id,
        )
        return event

    async def event_exists(self, provider: PaymentProvider, provider_event_id: str) -> bool:
        """Check if a payment event already exists."""
        provider_val = provider.value if isinstance(provider, PaymentProvider) else provider
        query = (
            self._db.collection(self._events_collection)
            .where("provider", "==", provider_val)
            .where("providerEventId", "==", provider_event_id)
            .limit(1)
        )

        docs = list(query.stream())
        return len(docs) > 0


class InMemoryDonationRepository(DonationRepositoryBase):
    """In-memory implementation for testing."""

    def __init__(self) -> None:
        self._donations: dict[str, Donation] = {}
        self._events: dict[str, PaymentEvent] = {}

    async def create(self, donation: Donation) -> Donation:
        self._donations[donation.id] = donation
        return donation

    async def get_by_id(self, donation_id: str) -> Donation | None:
        return self._donations.get(donation_id)

    async def get_by_provider_order_id(
        self, provider: PaymentProvider, provider_order_id: str
    ) -> Donation | None:
        provider_val = provider.value if isinstance(provider, PaymentProvider) else provider
        for donation in self._donations.values():
            if (donation.provider == provider_val
                    and donation.provider_order_id == provider_order_id):
                return donation
        return None

    async def update_status(
        self, donation_id: str, status: DonationStatus, completed_at: datetime | None = None
    ) -> Donation | None:
        donation = self._donations.get(donation_id)
        if not donation:
            return None

        status_val = status.value if isinstance(status, DonationStatus) else status
        updated = donation.model_copy(
            update={
                "status": status_val,
                "updated_at": datetime.now(UTC),
                "completed_at": completed_at,
            }
        )
        self._donations[donation_id] = updated
        return updated

    async def save_payment_event(self, event: PaymentEvent) -> PaymentEvent:
        self._events[event.id] = event
        return event

    async def event_exists(self, provider: PaymentProvider, provider_event_id: str) -> bool:
        provider_val = provider.value if isinstance(provider, PaymentProvider) else provider
        for event in self._events.values():
            if event.provider == provider_val and event.provider_event_id == provider_event_id:
                return True
        return False
