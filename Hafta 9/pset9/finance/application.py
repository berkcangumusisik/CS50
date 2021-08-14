import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime  # for date and time

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
'''
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
'''


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        pass1 = request.form.get("password")
        pass2 = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username is distinct
        if len(rows) != 0:
            # return apology("Username Already Taken", 403)
            return "<script>alert('Username Already Exists')</script>"

        # Ensuring the password is typed in correctly twice
        elif pass1 != pass2:
            return apology("passwords don't match!", 400)

        else:
            # Generating Hash of password
            password = generate_password_hash(pass1)

            # Inserting new user and hash
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)

            # Remember which user has logged in
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username", username=username)[0]["id"]

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index():
    # Show portfolio of stocks
    # Getting No of Shares of Each stock as A list of Dictionary
    stocks = db.execute("SELECT stock_symbol, no_shares FROM stocks WHERE user_id = ?", session["user_id"])

    # Getting the Cash of user
    total = cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Creating A list of Dictionary with Comp. name, Symbol, Price, Shares and Total
    stock_info = []

    for i in range(len(stocks)):
        # Looking up for the Price and name for a symbol
        stock_info.append(lookup(stocks[i]["stock_symbol"]))
    # Storing no. of Shares
        stock_info[i]["shares"] = stocks[i]["no_shares"]
    # Storing Total Value of Shares as USD
        stock_info[i]["total"] = usd(stock_info[i]["shares"] * stock_info[i]["price"])
    # Calculating Total of all the share values
        total += stock_info[i]["shares"] * stock_info[i]["price"]
    # Converting Price in USD
        stock_info[i]["price"] = usd(stock_info[i]["price"])

    return render_template("index.html", stocks=stock_info, cash=usd(cash), total=usd(total))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get stock information using Lookup Function
        stock = lookup(request.form.get("symbol"))

        # Check for Stock symbol
        if stock == None:
            return apology("Invalid Symbol", 400)

        else:
            return render_template("qouted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("qoute.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Looking for a stock
        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("Invalid Symbol")

        # Getting the number of shares user want
        shares = int(request.form.get("shares"))
        # Getting cash user have
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        # checking if user can afford or not
        req_amount = shares*stock["price"]
        if req_amount > cash:
            return apology("Can't Afford")

        prev_stocks = db.execute("SELECT no_shares FROM stocks WHERE user_id = ? AND stock_symbol = ?",
                                 session["user_id"], stock["symbol"])

        # Checking if user already own that stock
        if len(prev_stocks) != 0:
            # Getting no. of shares already exists
            prev_shares = prev_stocks[0]["no_shares"]
            # Updating the no. of shares
            db.execute("UPDATE stocks SET no_shares = ? WHERE user_id = ? AND stock_symbol = ?",
                       prev_shares+shares, session["user_id"], stock["symbol"])
            # Updating the cash
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash-req_amount, session["user_id"])

        # If deosn't own that stock Inserting a new row for that stock
        else:
            db.execute("INSERT INTO stocks (user_id, stock_symbol, no_shares) VALUES (?, ? , ?)",
                       session["user_id"], stock["symbol"], shares)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash-req_amount, session["user_id"])

        # Inserting data in History
        now = datetime.now()
        transacted = now.strftime("%H:%M:%S %d/%m/%Y")
        db.execute("INSERT INTO history (id, symbol, price, total, shares, datetime) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], usd(stock["price"]), usd(req_amount), shares, transacted)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        shares = int(request.form.get("shares"))
        if shares == 0:
            return redirect("/")

        # Looking for stock
        stock = lookup(request.form.get("symbol"))

        # Getting info on stocks owned
        prev_stocks = db.execute("SELECT no_shares FROM stocks WHERE user_id = ? AND stock_symbol = ?",
                                 session["user_id"], stock["symbol"])

        # Getting no. of shares already exists
        prev_shares = prev_stocks[0]["no_shares"]

        if shares > prev_shares:
            return apology("You don't have that many shares")

        # Getting the cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Cost of shares to sell
        amount = shares*stock["price"]

        # Updating the no. of shares
        db.execute("UPDATE stocks SET no_shares = ? WHERE user_id = ? AND stock_symbol = ?",
                   prev_shares-shares, session["user_id"], stock["symbol"])
        # Updating the cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash+amount, session["user_id"])

        # Inserting data in History
        now = datetime.now()
        transacted = now.strftime("%H:%M:%S %d/%m/%Y")
        db.execute("INSERT INTO history (id, symbol, price, total, shares, datetime) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], usd(stock["price"]), usd(amount), -shares, transacted)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        stocks = db.execute("SELECT stock_symbol, no_shares FROM stocks WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Getting the History
    stocks = db.execute(
        "SELECT symbol, shares, price, total, datetime FROM history WHERE id = ? ORDER BY sr DESC", session["user_id"])
    return render_template("history.html", stocks=stocks)


@app.route("/pchange", methods=["GET", "POST"])
@login_required
def pchange():
    """Change Password"""
    if request.method == "POST":

        #
        old = request.form.get("old")
        npass1 = request.form.get("pass1")
        npass2 = request.form.get("pass2")

        # Ensuring the password is typed in correctly twice
        if npass1 != npass2:
            return apology("Passwords Didn't match")

        # Query database for password
        hashed = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])[0]["hash"]

        if not check_password_hash(hashed, old):
            return apology("Incorrect Password")

        else:
            # Generating Hash of password
            npassword = generate_password_hash(npass1)

            # Updating new hash
            db.execute("UPDATE users SET hash = ? WHERE id = ?", npassword, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("pchange.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
