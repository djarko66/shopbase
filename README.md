# ShopBase

Flask reporting app for a shop database. Exposes read-only JSON
endpoints over customers, products, orders, payments, and shipments,
rendered in a simple dashboard.

## Setup

```bash
pip install flask mysql-connector-python
cp .env.example .env   # fill in your DB credentials
python app.py
```

Runs on http://localhost:5050.

## Endpoints

- `GET /api/customers`
- `GET /api/products`
- `GET /api/orders`
- `GET /api/payment/<order_id>`
- `GET /api/shipment/<order_id>`

## Stack

Flask, MySQL (mysql-connector-python)
