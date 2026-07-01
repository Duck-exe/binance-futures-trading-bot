# Binance Futures Testnet Trading Bot

## Overview

This project is a Python-based trading bot that places MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). The bot provides an interactive Command Line Interface (CLI), validates user inputs, logs API requests and responses, and handles API/network errors.

---

## Features

- Place MARKET orders
- Place LIMIT orders
- Supports BUY and SELL
- Interactive CLI (menus and prompts)
- Input validation
- Logging of API requests and responses
- Exception handling
- Binance Futures Testnet integration

---

## Requirements

- Python 3.x
- Binance Futures Testnet Account
- Binance Testnet API Key & Secret

---

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project directory.

```text
BINANCE_TESTNET_API_KEY=your_api_key
BINANCE_TESTNET_API_SECRET=your_api_secret
```

---

## Running the Program

Run:

```bash
python trading_bot.py
```

The program will guide you through the order creation process.

Example:

```
===================================
 Binance Futures Trading Bot
===================================

Enter Symbol (Example: BTCUSDT): BTCUSDT

Choose Order Side
1. BUY
2. SELL

Enter choice (1/2): 1

Choose Order Type
1. MARKET
2. LIMIT

Enter choice (1/2): 2

Enter Quantity:
0.001

Enter Limit Price:
120000
```

The bot then submits the order and prints:

```
==============================
ORDER REQUEST SUMMARY
==============================
Symbol      : BTCUSDT
Side        : BUY
Order Type  : LIMIT
Quantity    : 0.001
Price       : 120000

==============================
ORDER RESPONSE DETAILS
==============================
orderId        : 18216806746
status         : NEW
executedQty    : 0.0000
avgPrice       : None
price          : 120000.00

SUCCESS: Order placed successfully.
```

---

## Logging

All API requests, responses, and errors are stored in:

```
logs/trading_bot.log
```

---

## Assumptions

- Uses Binance Futures Testnet.
- Supports USDT-M Futures symbols.
- MARKET and LIMIT orders are supported.
- BUY and SELL operations are supported.

---

## Dependencies

- requests
- python-dotenv
