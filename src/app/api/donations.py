"""Donation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

import structlog

from app.models.donation import (
    CheckoutRequest,
    CheckoutResponse,
    DonationResponse,
    PaymentProvider,
)
from app.services.payment import (
    DonationNotFoundError,
    DuplicateEventError,
    InvalidSignatureError,
    PaymentService,
    PaymentServiceError,
)

logger = structlog.get_logger()

router = APIRouter(prefix="/api", tags=["donations"])


# Dependency injection placeholder - will be replaced with actual service
_payment_service: PaymentService | None = None


def get_payment_service() -> PaymentService:
    """Get the payment service instance."""
    if _payment_service is None:
        raise RuntimeError("PaymentService not initialized")
    return _payment_service


def set_payment_service(service: PaymentService) -> None:
    """Set the payment service instance (for initialization)."""
    global _payment_service
    _payment_service = service


@router.post("/donations/checkout", response_model=CheckoutResponse)
async def create_checkout(
    request: CheckoutRequest,
    service: PaymentService = Depends(get_payment_service),
) -> CheckoutResponse:
    """Create a checkout session for donation.

    Creates a new donation record and returns a redirect URL
    to the payment provider's checkout page.
    """
    logger.info(
        "Checkout request received",
        amount=request.amount,
        provider=request.provider.value,
        source=request.source,
    )

    try:
        response = await service.create_checkout(request)
        return response
    except PaymentServiceError as e:
        logger.error("Checkout creation failed", code=e.code, message=e.message)
        raise HTTPException(
            status_code=400 if e.code == "INVALID_ARGUMENT" else 503,
            detail={"error": e.code, "message": e.message},
        )


@router.get("/donations/{donation_id}", response_model=DonationResponse)
async def get_donation(
    donation_id: str,
    service: PaymentService = Depends(get_payment_service),
) -> DonationResponse:
    """Get donation status by ID."""
    try:
        return await service.get_donation(donation_id)
    except DonationNotFoundError:
        raise HTTPException(
            status_code=404,
            detail={"error": "DONATION_NOT_FOUND", "message": f"Donation not found: {donation_id}"},
        )


@router.post("/webhooks/paypay")
async def paypay_webhook(
    request: Request,
    service: PaymentService = Depends(get_payment_service),
) -> JSONResponse:
    """Receive PayPay webhook notifications.

    Verifies the signature and updates donation status.
    """
    body = await request.body()
    headers = dict(request.headers)

    logger.info("PayPay webhook received", content_length=len(body))

    try:
        await service.process_webhook(PaymentProvider.PAYPAY, headers, body)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except InvalidSignatureError as e:
        logger.warning("PayPay webhook signature invalid", error=e.message)
        return JSONResponse(
            status_code=401,
            content={"error": e.code, "message": e.message},
        )
    except DuplicateEventError as e:
        logger.info("PayPay webhook duplicate event", error=e.message)
        return JSONResponse(status_code=200, content={"status": "already_processed"})
    except PaymentServiceError as e:
        logger.error("PayPay webhook processing failed", code=e.code, message=e.message)
        return JSONResponse(
            status_code=400,
            content={"error": e.code, "message": e.message},
        )


@router.post("/webhooks/rakuten")
async def rakuten_webhook(
    request: Request,
    service: PaymentService = Depends(get_payment_service),
) -> JSONResponse:
    """Receive Rakuten Pay webhook notifications.

    Verifies the signature and updates donation status.
    """
    body = await request.body()
    headers = dict(request.headers)

    logger.info("Rakuten Pay webhook received", content_length=len(body))

    try:
        await service.process_webhook(PaymentProvider.RAKUTEN, headers, body)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except InvalidSignatureError as e:
        logger.warning("Rakuten Pay webhook signature invalid", error=e.message)
        return JSONResponse(
            status_code=401,
            content={"error": e.code, "message": e.message},
        )
    except DuplicateEventError as e:
        logger.info("Rakuten Pay webhook duplicate event", error=e.message)
        return JSONResponse(status_code=200, content={"status": "already_processed"})
    except PaymentServiceError as e:
        logger.error("Rakuten Pay webhook processing failed", code=e.code, message=e.message)
        return JSONResponse(
            status_code=400,
            content={"error": e.code, "message": e.message},
        )
