# SDA POS System

Point of Sale desktop app for small retail — **Python (Tkinter) + PostgreSQL**, structured with **MVC**.

## Highlights

- Role-based auth (Admin, Cashier, Manager)
- Sales and billing: search, cart, checkout
- Inventory: stock levels, search, restock
- Customer loyalty profiles and points
- Refunds against past transactions
- Sales history / reporting foundation

## Stack

| Layer | Tech |
|-------|------|
| UI | Python Tkinter |
| Architecture | MVC |
| Database | PostgreSQL |

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Configure PostgreSQL via project config / `.env` (never commit secrets).

## What this demonstrates

Production-minded desktop app structure: clear MVC boundaries, role checks, and core retail workflows.
