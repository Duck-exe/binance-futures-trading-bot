# ============================================================
# Binance Futures Testnet Trading Bot
#
# Features:
# - Place MARKET and LIMIT orders
# - Supports BUY and SELL orders
# - CLI using argparse
# - Input validation
# - Logging
# - Error handling
#
# Author: Dakshanya Maddala
# ============================================================

import argparse
import hashlib
import hmac
import logging
import os
import time
from decimal import Decimal
from logging.handlers import RotatingFileHandler
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

# ------------------------------------------------------------
# Load environment variables from .env file
# ------------------------------------------------------------
load_dotenv()


# ------------------------------------------------------------
# Configure Logger
# Logs all API requests and responses to logs/trading_bot.log
# ------------------------------------------------------------
def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)

    # Avoid duplicate log handlers
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            "logs/trading_bot.log",
            maxBytes=1_000_000,
            backupCount=3,
        )

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()


# ------------------------------------------------------------
# Validate positive numeric values
# ------------------------------------------------------------
def positive_number(value, field_name):
    """
    Ensures quantity and price are positive decimal values.
    """
    decimal_value = Decimal(str(value))

    if decimal_value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")

    return format(decimal_value, "f")


# ------------------------------------------------------------
# Parse command-line arguments
# ------------------------------------------------------------
def parse_arguments():
    """
    Interactive CLI Menu
    """

    print("\n===================================")
    print(" Binance Futures Trading Bot")
    print("===================================\n")

    symbol = input("Enter Symbol (Example: BTCUSDT): ").strip().upper()

    # BUY / SELL Menu
    while True:
        print("\nChoose Order Side")
        print("1. BUY")
        print("2. SELL")

        choice = input("Enter choice (1/2): ").strip()

        if choice == "1":
            side = "BUY"
            break
        elif choice == "2":
            side = "SELL"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # MARKET / LIMIT Menu
    while True:
        print("\nChoose Order Type")
        print("1. MARKET")
        print("2. LIMIT")

        choice = input("Enter choice (1/2): ").strip()

        if choice == "1":
            order_type = "MARKET"
            break
        elif choice == "2":
            order_type = "LIMIT"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Quantity Validation
    while True:
        quantity = input("\nEnter Quantity: ").strip()

        try:
            positive_number(quantity, "quantity")
            break
        except Exception as e:
            print(e)

    price = None

    if order_type == "LIMIT":
        while True:
            price = input("Enter Limit Price: ").strip()

            try:
                positive_number(price, "price")
                break
            except Exception as e:
                print(e)

    class Args:
        pass

    args = Args()
    args.symbol = symbol
    args.side = side
    args.order_type = order_type
    args.quantity = quantity
    args.price = price

    return args


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------
def main():

    args = parse_arguments()

    # Read API credentials from .env
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError(
            "Missing API credentials. Please configure your .env file."
        )

    # --------------------------------------------------------
    # Build request parameters
    # --------------------------------------------------------
    params = {
        "symbol": args.symbol.upper(),
        "side": args.side,
        "type": args.order_type,
        "quantity": positive_number(args.quantity, "quantity"),
        "timestamp": int(time.time() * 1000),
        "recvWindow": 5000,
    }

    # LIMIT orders require price and timeInForce
    if args.order_type == "LIMIT":

        if not args.price:
            raise ValueError("Price is required for LIMIT orders.")

        params["price"] = positive_number(args.price, "price")
        params["timeInForce"] = "GTC"

    # --------------------------------------------------------
    # Generate HMAC SHA256 signature
    # --------------------------------------------------------
    query_string = urlencode(params)

    signature = hmac.new(
        api_secret.encode(),
        query_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    params["signature"] = signature

    # Log request
    logger.info("Request %s", params)

    # --------------------------------------------------------
    # Print Order Request Summary
    # --------------------------------------------------------
    print("\n==============================")
    print("ORDER REQUEST SUMMARY")
    print("==============================")

    print(f"Symbol      : {args.symbol.upper()}")
    print(f"Side        : {args.side}")
    print(f"Order Type  : {args.order_type}")
    print(f"Quantity    : {args.quantity}")

    if args.order_type == "LIMIT":
        print(f"Price       : {args.price}")

    # --------------------------------------------------------
    # Send request to Binance Futures Testnet
    # --------------------------------------------------------
    response = requests.post(
        "https://testnet.binancefuture.com/fapi/v1/order",
        headers={
            "X-MBX-APIKEY": api_key,
        },
        params=params,
        timeout=15,
    )

    data = response.json()

    # Log response
    logger.info("Response %s", data)

    # --------------------------------------------------------
    # Print Order Response
    # --------------------------------------------------------
    print("\n==============================")
    print("ORDER RESPONSE DETAILS")
    print("==============================")

    for field in [
        "orderId",
        "status",
        "executedQty",
        "avgPrice",
        "price",
    ]:
        print(f"{field:15}: {data.get(field)}")

    # --------------------------------------------------------
    # Print Final Status
    # --------------------------------------------------------
    if response.ok:
        print("\nSUCCESS: Order placed successfully.")
    else:
        print("\nFAILURE:", data)


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
