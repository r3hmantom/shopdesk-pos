# SDA POS System

A Point of Sale (POS) system built with Python (Tkinter) and PostgreSQL, following the MVC (Model-View-Controller) architecture.

## Features

- **User Authentication**: Login and Registration with role-based access (Admin, Cashier, Manager).
- **Sales & Billing**: Product search, cart management, and checkout.
- **Inventory Management**: View stock levels, search products, and restock items.
- **Customer Loyalty**: Manage customer profiles and loyalty points.
- **Refunds**: Process refunds for past transactions.
- **Reporting**: (Basic structure implemented via Sales History).

## Project Structure

```
src/
├── controllers/    # Business logic and communication between Model and View
├── models/         # Database interactions (Users, Products, Sales, Customers)
├── views/          # GUI components (Tkinter frames)
├── utils/          # Helper functions
├── database.py     # Database connection and initialization
├── config.py       # Configuration loading
└── main.py         # Application entry point
```

## Prerequisites

- Python 3.x
- PostgreSQL

## Setup Instructions

1.  **Clone the repository** (if applicable) or navigate to the project folder.

2.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Setup**:

    - Ensure PostgreSQL is running.
    - Create a database named `sda_pos` (or whatever you prefer).
    - Create a `.env` file in the root directory (copy from `.env.example`):
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` with your database credentials:
      ```
      DB_NAME=sda_pos
      DB_USER=postgres
      DB_PASSWORD=your_password
      DB_HOST=localhost
      DB_PORT=5432
      ```

4.  **Run the Application**:
    ```bash
    python -m src.main
    ```
    _Note: Run from the root directory._

## Default Credentials

On the first run, the system will create an Admin user if one doesn't exist:

- **Username**: `admin`
- **Password**: `admin123`

## Architecture

This project uses the **MVC Pattern**:

- **Model**: Handles data logic and database queries (e.g., `src/models/product_model.py`).
- **View**: Handles the UI display (e.g., `src/views/sales_view.py`).
- **Controller**: Handles user input and orchestrates the flow (e.g., `src/controllers/auth_controller.py`).

## License

[License Name]
