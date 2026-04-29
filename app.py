from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
from abc import ABC, abstractmethod   # # Abstraction

app = Flask(__name__)
app.secret_key = "secret123"


# ====== ABSTRACT CLASS ======
class Person(ABC):
    def __init__(self, name, user_id):
        self._name = name
        self._user_id = user_id

    @abstractmethod
    def get_role(self):
        pass


# ====== USER (INHERITANCE) ======
class User(Person):
    def __init__(self, name, user_id, role):
        super().__init__(name, user_id)  # # inheritance using super
        self.__role = role

    # # ENCAPSULATION (getters)
    def get_name(self):
        return self._name

    def get_user_id(self):
        return self._user_id

    def get_role(self):
        return self.__role

    # # setters
    def set_name(self, name):
        self._name = name

    def set_role(self, role):
        self.__role = role


# ====== PRODUCT ======
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


# ====== CART ITEM ======
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

    # # POLYMORPHISM (method overriding example later)
    def get_total(self):
        return self.__product.get_price() * self.__qty


# ====== DISCOUNT CART ITEM (POLYMORPHISM - OVERRIDING) ======
class DiscountCartItem(CartItem):
    def __init__(self, product, qty=1, discount=0.1):
        super().__init__(product, qty)
        self.__discount = discount

    def get_total(self):  # # method overriding
        original = super().get_total()
        return original - (original * self.__discount)


# ====== SALE ======
class Sale:
    def __init__(self, items, cash):
        self.__items = items
        self.__cash = cash
        self.__total = self.calculate_total()  # # polymorphism usage
        self.__change = cash - self.__total
        self.__date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # # POLYMORPHISM (method overloading style using default param)
    def calculate_total(self, extra_fee=0):
        return sum(i.get_total() for i in self.__items) + extra_fee

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


# ====== STORE ======
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

    product = next((p for p in store.get_products() if p.get_name() == name), None)

    if not product:
        return jsonify({"error": "Product not found"}), 404  # # FIXED ERROR HANDLING

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

        # # Example: use polymorphism (normal vs discounted)
        if c["qty"] >= 5:
            items.append(DiscountCartItem(product, c["qty"]))  # # overriding used
        else:
            items.append(CartItem(product, c["qty"]))

    sale = Sale(items, cash)

    if sale.get_cash() < sale.get_total():
        return "Not enough cash!"

    store.add_sale(sale)

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
    sales_data = [
        {
            "total": s.get_total(),
            "date": s.get_date()
        }
        for s in store.get_sales()
    ]

    return render_template("sales-summary.html", sales=sales_data)


# ====== LOGOUT ======
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ====== RUN ======
if __name__ == "__main__":
    app.run(debug=True)
