import os
import urllib
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/inbox")
@login_required
def inbox():
    """Show portfolio of stocks"""
    if request.method == "GET":
        userId = session["user_id"]
        usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        username = usernameDB[0]["username"]
        emails = db.execute("SELECT * FROM emails WHERE recipient = ?", username)
        return render_template("index.html", emails=emails)


@app.route("/junk", methods=["GET", "POST"])
@login_required
def junk():
    """junk page"""
    if request.method == "GET":
        userId = session["user_id"]
        senderDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        sender = senderDB[0]["username"]
        return render_template("junk.html", sender=sender)
    else:
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not sender or not recipient or not subject or not body:
            return apology("No empty Fields")

        db.execute("INSERT INTO emails (sender, recipient, subject, body) VALUES (?, ?, ?, ?)", sender, recipient, subject, body)

        return redirect("/sentbox")

@app.route("/sentbox")
@login_required
def sentbox():
    """Show history of transactions"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", username)
    return render_template("index.html", emails=emails)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/junk")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/email", methods=["POST"])
@login_required
def email():
    """Get stock quote."""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        emailDetail = emailDetailDB[0]
        return render_template("email.html", emailDetail=emailDetail)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return apology("Must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("Must provide password", 400)

        elif password != confirmation:
            return apology("Password do not match!", 400)

        # Query database for username
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?);", username, generate_password_hash(password))
        except:
            return apology("Username is taken, please try another username", 400)

        session['user_id'] = new_user

        flash("Registered Successful!")
        # Redirect user to home page
        return redirect("/login")

    else:
        return render_template("register.html")
