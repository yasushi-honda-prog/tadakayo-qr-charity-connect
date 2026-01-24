#!/usr/bin/env python3
"""Test script for PayPay Sandbox integration.

Usage:
    export PAYPAY_API_KEY="your_api_key"
    export PAYPAY_API_SECRET="your_api_secret"
    python scripts/test_paypay_sandbox.py

This script tests the PayPay SDK integration with sandbox credentials.
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.adapters.base import CheckoutSessionInput
from app.adapters.paypay import PayPayAdapter


async def main():
    """Test PayPay Sandbox connection."""
    api_key = os.environ.get("PAYPAY_API_KEY")
    api_secret = os.environ.get("PAYPAY_API_SECRET")
    merchant_id = os.environ.get("PAYPAY_MERCHANT_ID")

    if not api_key or not api_secret:
        print("Error: PAYPAY_API_KEY and PAYPAY_API_SECRET environment variables required")
        print("\nUsage:")
        print('  export PAYPAY_API_KEY="your_api_key"')
        print('  export PAYPAY_API_SECRET="your_api_secret"')
        print('  export PAYPAY_MERCHANT_ID="your_merchant_id"  # Optional but recommended')
        print("  python scripts/test_paypay_sandbox.py")
        sys.exit(1)

    print("=" * 60)
    print("PayPay Sandbox Integration Test")
    print("=" * 60)
    print(f"API Key: {api_key[:10]}...")
    print(f"API Secret: {api_secret[:10]}...")
    print(f"Merchant ID: {merchant_id or '(not set)'}")
    print()

    # Initialize adapter with real credentials
    adapter = PayPayAdapter(
        api_key=api_key,
        api_secret=api_secret,
        merchant_id=merchant_id,
        production_mode=False,  # Sandbox mode
    )

    # Create a test checkout session
    input_data = CheckoutSessionInput(
        amount=100,  # 100 JPY test amount
        currency="JPY",
        order_id="test_order_001",
        return_url="https://example.com/thanks",
        cancel_url="https://example.com/cancel",
        description="PayPay Sandbox Test",
    )

    print("Creating checkout session...")
    print(f"  Amount: {input_data.amount} {input_data.currency}")
    print(f"  Order ID: {input_data.order_id}")
    print()

    try:
        result = await adapter.create_checkout_session(input_data)

        print("SUCCESS! Checkout session created:")
        print(f"  Redirect URL: {result.redirect_url}")
        print(f"  Provider Order ID: {result.provider_order_id}")
        print(f"  Expires At: {result.expires_at}")
        print()
        print("Open the redirect URL in a browser to test the payment flow.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
