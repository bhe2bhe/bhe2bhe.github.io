import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create a SQLite database object
db = SQL("sqlite:///mod.db")

# Define the User table
db.execute(
    "CREATE TABLE users ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "username TEXT NOT NULL,"
    "email TEXT NOT NULL"
    ")"
)

# Define the index route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Define the login route
@app.route("/register", methods=["POST"])
def login():
    # Get the email and password from the form data
    email = request.form.get("email")
    password = request.form.get("password")

    # Perform login logic (validate user credentials)
    user = db.execute("SELECT * FROM users WHERE email = :email", email=email).fetchone()

    if user and check_password_hash(user["password"], password):
        # If the credentials are valid, redirect to the profile page
        return redirect(url_for("profile"))
    else:
        # If the credentials are invalid, show an error message
        error_message = "Invalid email or password. Please try again."
        return render_template("index.html", error_message=error_message)

# Define the register route
@app.route("/register", methods=["POST"])
def register():
    # Get the user input from the form data
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)

    # Insert the user data into the database
    db.execute(
        "INSERT INTO users (username, email, password) VALUES (:username, :email, :hashed_password)",
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.commit()

    # Redirect to the profile page after successful registration
    return redirect(url_for("profile"))

# Route for the profile page
@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")

@app.route("/users", methods=["GET"])
def get_users():
    users = db.execute("SELECT * FROM users")
    return render_template("users.html", users=users)


if __name__ == "__main__":
    app.run()
