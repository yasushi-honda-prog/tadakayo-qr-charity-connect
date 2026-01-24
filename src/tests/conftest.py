"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.adapters.paypay import PayPayAdapter
from app.adapters.rakuten import RakutenPayAdapter
from app.main import app, init_services
from app.models.donation import PaymentProvider
from app.repositories.donation import InMemoryDonationRepository
from app.services.payment import PaymentService
from app.api.donations import set_payment_service


@pytest.fixture
def in_memory_repository():
    """Create an in-memory repository for testing."""
    return InMemoryDonationRepository()


@pytest.fixture
def paypay_adapter():
    """Create a PayPay adapter for testing."""
    return PayPayAdapter(
        webhook_secret="test_paypay_secret",
        production_mode=False,
    )


@pytest.fixture
def rakuten_adapter():
    """Create a Rakuten Pay adapter for testing."""
    return RakutenPayAdapter(
        webhook_secret="test_rakuten_secret",
        sandbox=True,
    )


@pytest.fixture
def payment_service(in_memory_repository, paypay_adapter, rakuten_adapter):
    """Create a payment service for testing."""
    adapters = {
        PaymentProvider.PAYPAY: paypay_adapter,
        PaymentProvider.RAKUTEN: rakuten_adapter,
    }
    return PaymentService(repository=in_memory_repository, adapters=adapters)


@pytest.fixture
def test_client(payment_service):
    """Create a test client with initialized services."""
    set_payment_service(payment_service)
    return TestClient(app)
