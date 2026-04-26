from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"


# ====== MODELS ======

class User:
    def __init__(self, name, user_id, role):
        self.__name = name
        self.__user_id = user_id
        self.__role = role

    # GETTERS
    def get_name(self):
        return self.__name

    def get_user_id(self):
        return self.__user_id

    def get_role(self):
        return self.__role

    # SETTERS
    def set_name(self, name):
        self.__name = name

    def set_role(self, role):
        self.__role = role


class Product:
    def __init__(self, name, category, price):
        self.__name = name
        self.__category = category
        self.__price = price

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_price(self):
        return self.__price


class CartItem:
    def __init__(self, product, qty=1):
        self.__product = product
        self.__qty = qty

    def get_product(self):
        return self.__product

    def get_qty(self):
        return self.__qty

    def set_qty(self, qty):
        self.__qty = qty

    def get_total(self):
        return self.__product.get_price() * self.__qty


class Sale:
    def __init__(self, items, cash):
        self.__items = items
        self.__cash = cash
        self.__total = sum(i.get_total() for i in items)
        self.__change = cash - self.__total
        self.__date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_items(self):
        return self.__items

    def get_total(self):
        return self.__total

    def get_cash(self):
        return self.__cash

    def get_change(self):
        return self.__change

    def get_date(self):
        return self.__date


class Store:
    def __init__(self):
        self.__users = []
        self.__products = []
        self.__sales = []

    # USERS
    def add_user(self, user):
        self.__users.append(user)

    def find_user(self, user_id):
        for u in self.__users:
            if u.get_user_id() == user_id:
                return u
        return None

    # PRODUCTS
    def add_product(self, product):
        self.__products.append(product)

    def get_products(self):
        return self.__products

    # SALES
    def add_sale(self, sale):
        self.__sales.append(sale)

    def get_sales(self):
        return self.__sales


# ====== STORE INSTANCE ======
store = Store()

# preload products
store.add_product(Product("Rice", "Groceries", 45))
store.add_product(Product("Soft Drinks", "Beverages", 18))
store.add_product(Product("Canned Sardines", "Groceries", 20))
store.add_product(Product("Chips", "Snacks", 15))
store.add_product(Product("Detergent", "Household", 25))


# ====== LOGIN ======
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("userId")

        user = store.find_user(user_id)

        if not user:
            return "User not found!"

        session["user"] = user.get_user_id()
        session["cart"] = []

        return redirect("/sales")

    return render_template("login.html")


# ====== REGISTER ======
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    user_id = request.form.get("userId")
    role = request.form.get("role")

    if store.find_user(user_id):
        return "User already exists!"

    store.add_user(User(name, user_id, role))
    return redirect("/")


# ====== SALES ======
@app.route("/sales")
def sales_page():
    products = store.get_products()

    # convert objects → dict for HTML
    product_list = [
        {
            "name": p.get_name(),
            "category": p.get_category(),
            "price": p.get_price()
        }
        for p in products
    ]

    return render_template("sales.html", products=product_list)


# ====== ADD TO CART ======
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json
    name = data["name"]

    # find product
    product = next((p for p in store.get_products() if p.get_name() == name), None)

    cart = session.get("cart", [])

    found = next((i for i in cart if i["name"] == name), None)

    if found:
        found["qty"] += 1
    else:
        cart.append({
            "name": product.get_name(),
            "price": product.get_price(),
            "qty": 1
        })

    session["cart"] = cart
    return jsonify(cart)


# ====== PAYMENT ======
@app.route("/payment")
def payment():
    cart = session.get("cart", [])

    total = sum(i["price"] * i["qty"] for i in cart)

    return render_template("payment.html", total=total)


# ====== PAY ======
@app.route("/pay", methods=["POST"])
def pay():
    cash = float(request.form.get("cash"))
    cart_data = session.get("cart", [])

    items = []

    for c in cart_data:
        product = Product(c["name"], "", c["price"])
        items.append(CartItem(product, c["qty"]))

    sale = Sale(items, cash)

    if sale.get_cash() < sale.get_total():
        return "Not enough cash!"

    store.add_sale(sale)

    # convert sale to dict for template
    session["lastSale"] = {
        "items": [
            {
                "name": i.get_product().get_name(),
                "qty": i.get_qty(),
                "price": i.get_product().get_price()
            }
            for i in sale.get_items()
        ],
        "total": sale.get_total(),
        "cash": sale.get_cash(),
        "change": sale.get_change(),
        "date": sale.get_date()
    }

    session["cart"] = []

    return redirect("/receipt")


# ====== RECEIPT ======
@app.route("/receipt")
def receipt():
    sale = session.get("lastSale")
    return render_template("receipt.html", sale=sale)


# ====== SUMMARY ======
@app.route("/summary")
def summary():
    sales_data = []

    for s in store.get_sales():
        sales_data.append({
            "total": s.get_total(),
            "date": s.get_date()
        })

    return render_template("sales-summary.html", sales=sales_data)


# ====== LOGOUT ======
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ====== RUN ======
if __name__ == "__main__":
    app.run(debug=True)
