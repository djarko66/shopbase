import os
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME", "shopbase")
    )


def query(sql, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    cols = [d[0] for d in cur.description]
    rows = [list(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return cols, rows


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/customers")
def customers():
    cols, rows = query("""
        SELECT customer_id, first_name, last_name, email, phone,
               registration_date, is_active
        FROM Customer
    """)
    return jsonify({"cols": cols, "rows": [[str(v) for v in r] for r in rows]})


@app.route("/api/products")
def products():
    cols, rows = query("""
        SELECT product_id, name, price, stock_quantity, is_available
        FROM Product
    """)
    return jsonify({"cols": cols, "rows": [[str(v) for v in r] for r in rows]})


@app.route("/api/orders")
def orders():
    cols, rows = query("""
        SELECT Orders.order_id,
               Customer.first_name,
               Customer.last_name,
               Orders.order_date,
               Orders.status,
               Orders.total_amount
        FROM Orders
        JOIN Customer ON Orders.customer_id = Customer.customer_id
    """)
    return jsonify({"cols": cols, "rows": [[str(v) for v in r] for r in rows]})


@app.route("/api/payment/<int:order_id>")
def payment(order_id):
    cols, rows = query("""
        SELECT Orders.order_id, Payment.method,
               Payment.status, Payment.amount, Payment.paid_at
        FROM Payment
        JOIN Orders ON Payment.order_id = Orders.order_id
        WHERE Orders.order_id = %s
    """, (order_id,))
    return jsonify({"cols": cols, "rows": [[str(v) for v in r] for r in rows]})


@app.route("/api/shipment/<int:order_id>")
def shipment(order_id):
    cols, rows = query("""
        SELECT Orders.order_id, Courier.company_name,
               Shipment.tracking_number, Shipment.status
        FROM Shipment
        JOIN Orders  ON Shipment.order_id  = Orders.order_id
        JOIN Courier ON Shipment.courier_id = Courier.courier_id
        WHERE Orders.order_id = %s
    """, (order_id,))
    return jsonify({"cols": cols, "rows": [[str(v) for v in r] for r in rows]})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
