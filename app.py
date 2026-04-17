from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"


# ====== MODELS ======

class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


products = [
    Product("Rice", 45, "Groceries"),
    Product("Soda", 18, "Beverages"),
    Product("Chips", 15, "Snacks"),
    Product("Detergent", 25, "Household"),
    Product("Soap", 12, "Household")
]


# ====== LOGIN ======

VALID_USER_ID = "1001"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["user_id"]

        if user_id == VALID_USER_ID:
            session["user"] = user_id
            session["cart"] = {}
            return redirect("/products")
        else:
            return render_template("login.html", error="Invalid User ID")

    return render_template("login.html")


# ====== PRODUCTS ======

@app.route("/products")
def show_products():
    if "user" not in session:
        return redirect("/")

    return render_template("products.html", products=products)


@app.route("/add/<int:index>")
def add_to_cart(index):
    cart = session.get("cart", {})

    product = products[index]
    name = product.name

    if name in cart:
        cart[name]["qty"] += 1
    else:
        cart[name] = {
            "price": product.price,
            "qty": 1
        }

    session["cart"] = cart
    return redirect("/products")


@app.route("/remove/<name>")
def remove_from_cart(name):
    cart = session.get("cart", {})

    if name in cart:
        cart[name]["qty"] -= 1
        if cart[name]["qty"] <= 0:
            del cart[name]

    session["cart"] = cart
    return redirect("/cart")


# ====== CART ======

@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    total = sum(item["price"] * item["qty"] for item in cart.values())

    return render_template("cart.html", cart=cart, total=total)


# ====== CHECKOUT ======

@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", {})
    total = sum(item["price"] * item["qty"] for item in cart.values())

    cash = float(request.form["cash"])

    if cash < total:
        return "Insufficient cash!"

    change = cash - total

    session["cart"] = {}

    return render_template("receipt.html",
                           cart=cart,
                           total=total,
                           cash=cash,
                           change=change)


# ====== RUN ======

if __name__ == "__main__":
    app.run(debug=True)
