# ShopDesk POS

Desktop point-of-sale app for small retail. Built with **Python (Tkinter) + PostgreSQL**, structured with **MVC**.

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

Clear MVC boundaries, role checks, and core retail workflows in a desktop app.
