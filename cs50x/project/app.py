import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Apply helpers.py
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# For inbox/homepage
@app.route("/", methods=["GET", "POST"])
@login_required
def inbox():

    user_id = session["user_id"]
    username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_db[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE receiver = ?", username)
    return render_template("index.html", emails=emails)

# To create new email
@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "GET":
        user_id = session["user_id"]
        sender_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        sender = sender_db[0]["username"]
        return render_template("create.html", sender=sender)

    else:
        sender = request.form.get("sender")
        receiver = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if sender == "":
            return apology("Invalid Sender")

        if receiver == "":
            return apology("Invalid Recipient")

        if subject == "":
            return apology("Invalid Subject")

        if body == "":
            return apology("Invalid Body of Message")

        db.execute("INSERT INTO emails (sender, receiver, subject, body) VALUES(?, ?, ?, ?)", sender, receiver, subject, body)

        return redirect("index.html")

# To go to sent email inbox
@app.route("/index", methods=["GET", "POST"])
@login_required
def sent():

    user_id = session["user_id"]
    username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_db[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", username)
    return render_template("index.html", emails=emails)

# To view ALL emails
@app.route("/email", methods=["GET", "POST"])
@login_required
def view_email():

    if request.method == "POST":
        email_id = request.form.get("email_id")
        email_detail_db = db.execute("SELECT * FROM emails WHERE id = ?", email_id)
        email_detail = email_detail_db[0]
        return render_template("email.html", email_detail=email_detail)

# To reply to an email in inbox
@app.route("/reply", methods=["GET", "POST"])
@login_required
def reply():

    if request.method == "POST":
        email_id = request.form.get("email_id")
        email_detail_db = db.execute("SELECT * FROM emails WHERE id = ?", email_id)
        email_detail = email_detail_db[0]
        return render_template("reply.html", email_detail=email_detail)

# To make sure user logs in properly
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# To make sure user properl logs out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# To make sure user is properly registered
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if email == "":
            return apology("Invalid Email")

        if password == "":
            return apology("Invalid Password")

        if confirmation == "":
            return apology("Invalid Password Confirmation")

        if password != confirmation:
            return apology("Passwords not matching")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", email, hash)
        except:
            return apology("Invalid Email. Name already exists")

        session["user_id"] = new_user

        return redirect("/")