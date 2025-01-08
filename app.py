from flask import Flask, render_template, request, redirect, session, Response
# import sqlite3
# uncomment this import for local testing
# import config
import os, sqlalchemy
from google.cloud.sql.connector import Connector

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_APP_SECRET")  # Replace with a secure secret key
connector = Connector()

# Initialize the db connection
def getconn():
    conn = connector.connect(
        os.environ.get("GLCOUD_SQL_CONNECTION_STRING"),
        "pymysql",
        user = os.environ.get("GLCOUD_SQL_APP_USER"),
        password = os.environ.get("GLCOUD_SQL_APP_PASSWORD"),
        db = os.environ.get("GLCOUD_SQL_DATABASE")
    )
    return conn

def init_db():
    with pool.connect() as db_conn:
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                donation REAL NOT NULL,
                total_price REAL NOT NULL,
                payment_method TEXT NOT NULL,
                delivery_location TEXT NOT NULL,
                other_instructions TEXT,
                scout TEXT,
                troop TEXT,
                village TEXT
            );
        """)
    
    # with sqlite3.connect("orders.db") as conn:
    #     conn.execute("""
    #         CREATE TABLE IF NOT EXISTS orders (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             first_name TEXT NOT NULL,
    #             last_name TEXT NOT NULL,
    #             address TEXT NOT NULL,
    #             phone TEXT NOT NULL,
    #             email TEXT NOT NULL,
    #             quantity INTEGER NOT NULL,
    #             donation REAL NOT NULL,
    #             total_price REAL NOT NULL,
    #             payment_method TEXT NOT NULL,
    #             delivery_location TEXT NOT NULL,
    #             other_instructions TEXT,
    #             scout TEXT,
    #             troop TEXT,
    #             village TEXT
    #         )
    #     """)


# Save order to the database
def save_order(data):
    # with sqlite3.connect("orders.db") as conn:
    with pool.connect() as conn:
        conn.execute("""
            INSERT INTO orders (first_name, last_name, address, phone, email, quantity, donation, total_price, payment_method, delivery_location, other_instructions, scout, troop, village)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data)


def check_auth(username, password):
    """Validate username and password."""
    return username == os.environ.get("USERNAME") and password == os.environ.get("PASSWORD")

def authenticate():
    """Sends a 401 response with a Basic Auth prompt."""
    return Response(
        "Login required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

@app.before_request
def require_auth():
    """Require authentication for all routes."""
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Collect form data
        scout = request.form["scout"]
        troop = request.form["troop"]
        village = request.form["village"]
        session["scout"] = scout
        session["troop"] = troop
        session["village"] = request.form.get("village")

        quantity = int(request.form["quantity"] or 0)
        donation = float(request.form["donation"] or 0)
        total_price = quantity * 6 + donation

        data = (
            request.form["first_name"],
            request.form["last_name"],
            request.form["address"],
            request.form["phone"],
            request.form["email"],
            quantity,
            donation,
            total_price,
            request.form["payment_method"],
            request.form["delivery_location"],
            request.form.get("other_instructions", ""),
            scout,
            troop,
            village
        )
        save_order(data)
        return redirect("/")
    
    # Pass last entered scout and troop values to the form
    return render_template(
        "form.html", 
        scout=session.get("scout", ""), 
        troop=session.get("troop", ""),
        village=session.get("village", ""),
        form = form,
        API_KEY = os.environ.get("GCLOUD_PLACES_API_KEY")
    )

if __name__ == "__main__":
    # create a connection pool for query execution
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn
    )

    # ensure the table exists
    init_db()

    #execute the main app so we are ready to take orders
    app.run(host="0.0.0.0", port=8080, debug=True)
