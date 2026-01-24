"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.adapters.paypay import PayPayAdapter
from app.adapters.rakuten import RakutenPayAdapter
from app.api.donations import router as donations_router
from app.api.donations import set_payment_service
from app.config import settings
from app.models.donation import PaymentProvider
from app.repositories.donation import FirestoreDonationRepository, InMemoryDonationRepository
from app.services.payment import PaymentService

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()


def init_services() -> None:
    """Initialize application services."""
    # Use in-memory repository for sandbox, Firestore for production
    if settings.environment == "sandbox":
        repository = InMemoryDonationRepository()
        logger.info("Using in-memory repository for sandbox environment")
    else:
        repository = FirestoreDonationRepository(project_id=settings.project_id)
        logger.info("Using Firestore repository", project_id=settings.project_id)

    # Initialize payment adapters (mock mode for now)
    adapters = {
        PaymentProvider.PAYPAY: PayPayAdapter(sandbox=True),
        PaymentProvider.RAKUTEN: RakutenPayAdapter(sandbox=True),
    }

    # Create and set payment service
    payment_service = PaymentService(repository=repository, adapters=adapters)
    set_payment_service(payment_service)

    logger.info("Services initialized", environment=settings.environment)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    init_services()
    yield


app = FastAPI(
    title="QR Payment API",
    description="タダカヨ QRチャリティ・コネクト 決済API",
    version="0.1.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)

# Include routers
app.include_router(donations_router)

# Static files directory
STATIC_DIR = Path(__file__).parent / "static"

# Mount static files (for CSS, JS, images if needed)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/donate")
async def donate_page() -> FileResponse:
    """Serve the donation amount selection page."""
    return FileResponse(STATIC_DIR / "donate.html")


@app.get("/thanks")
async def thanks_page() -> FileResponse:
    """Serve the thank you page."""
    return FileResponse(STATIC_DIR / "thanks.html")


@app.get("/cancel")
async def cancel_page() -> FileResponse:
    """Serve the cancellation page."""
    return FileResponse(STATIC_DIR / "cancel.html")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy", "environment": settings.environment}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "QR Payment API", "version": "0.1.0"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """Global exception handler."""
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
    )
