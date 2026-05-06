""""
SBPOSS - Small Business Point of Sale System
Developed with python Flask, HTML, CSS
Applies OOP 4 Pillars: Abstraction, Encapsulation, Inheritance, Polymorphism
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
import uuid

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "sbpos_secret_key_2024"

# =============================================================================
# OOP PILLAR 1: ABSTRACTION - Abstract Base Classes define contracts
# =============================================================================

class Entity(ABC):
    """Abstract base class for all business entities."""

    @abstractmethod
    def get_details(self) -> Dict:
        """Return entity details as dictionary."""
        pass

    @abstractmethod
    def get_display_name(self) -> str:
        """Return human-readable name."""
        pass


class POSOperations(ABC):
    """Abstract interface defining all POS system operations."""

    @abstractmethod
    def get_products(self, search: Optional[str] = None, category: Optional[str] = None) -> List:
        pass

    @abstractmethod
    def add_to_cart(self, product_id: str, quantity: int = 1) -> bool:
        pass

    @abstractmethod
    def update_cart_quantity(self, product_id: str, quantity: int) -> bool:
        pass

    @abstractmethod
    def remove_from_cart(self, product_id: str) -> bool:
        pass

    @abstractmethod
    def get_cart_total(self) -> float:
        pass

    @abstractmethod
    def checkout(self, cash_amount: float) -> Optional[object]:
        pass

    @abstractmethod
    def get_daily_summary(self) -> Dict:
        pass


class ReceiptGenerator(ABC):
    """Abstract class for receipt generation strategies."""

    @abstractmethod
    def generate(self, transaction) -> str:
        """Generate receipt output from transaction."""
        pass


# =============================================================================
# OOP PILLAR 2: ENCAPSULATION - Data hiding with private attributes
# =============================================================================

class Product(Entity):
    """Encapsulated Product entity with controlled access to attributes."""

    def __init__(self, product_id: str, name: str, price: float, category: str, stock: int):
        self.__id = product_id
        self.__name = name
        self.__price = price
        self.__category = category
        self.__stock = stock

    # Getters (read-only access to private fields)
    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def category(self) -> str:
        return self.__category

    @property
    def stock(self) -> int:
        return self.__stock

    # Controlled modifier with validation
    def reduce_stock(self, quantity: int) -> bool:
        if self.__stock >= quantity > 0:
            self.__stock -= quantity
            return True
        return False

    def get_details(self) -> Dict:
        return {
            "id": self.__id,
            "name": self.__name,
            "price": self.__price,
            "category": self.__category,
            "stock": self.__stock
        }

    def get_display_name(self) -> str:
        return f"{self.__name} (₱{self.__price:.2f})"


class CartItem:
    """Encapsulated cart item linking Product to purchase quantity."""

    def __init__(self, product: Product, quantity: int):
        self.__product = product
        self.__quantity = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def update_quantity(self, quantity: int) -> bool:
        if quantity > 0:
            self.__quantity = quantity
            return True
        return False

    def get_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def get_details(self) -> Dict:
        return {
            "product": self.__product.get_details(),
            "quantity": self.__quantity,
            "subtotal": self.get_subtotal()
        }


class Transaction(Entity):
    """Encapsulated Transaction entity representing a completed sale."""

    def __init__(self, items: List[CartItem], cash_given: float):
        self.__id = str(uuid.uuid4())[:8].upper()
        self.__date = datetime.now()
        self.__items = items.copy()
        self.__cash_given = cash_given
        self.__total = sum(item.get_subtotal() for item in items)
        self.__change = cash_given - self.__total

    @property
    def id(self) -> str:
        return self.__id

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def items(self) -> List[CartItem]:
        return self.__items.copy()

    @property
    def total(self) -> float:
        return self.__total

    @property
    def cash_given(self) -> float:
        return self.__cash_given

    @property
    def change(self) -> float:
        return self.__change

    def get_details(self) -> Dict:
        return {
            "id": self.__id,
            "date": self.__date.strftime("%Y-%m-%d %H:%M:%S"),
            "items": [item.get_details() for item in self.__items],
            "total": self.__total,
            "cash_given": self.__cash_given,
            "change": self.__change
        }

    def get_display_name(self) -> str:
        return f"Transaction {self.__id} - ₱{self.__total:.2f}"


class User(Entity):
    """Encapsulated User entity for authentication."""

    def __init__(self, username: str, password: str, full_name: str):
        self.__username = username
        self.__password = password
        self.__full_name = full_name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def full_name(self) -> str:
        return self.__full_name

    def authenticate(self, username: str, password: str) -> bool:
        return self.__username == username and self.__password == password

    def get_details(self) -> Dict:
        return {
            "username": self.__username,
            "full_name": self.__full_name
        }

    def get_display_name(self) -> str:
        return self.__full_name


# =============================================================================
# OOP PILLAR 3: INHERITANCE - Derived classes extend base functionality
# =============================================================================

class BasePOS(POSOperations):
    """Base POS class with common functionality. Inherited by concrete implementations."""

    def __init__(self):
        self._products: List[Product] = []
        self._cart: List[CartItem] = []
        self._transactions: List[Transaction] = []
        self._initialize_products()

    def _initialize_products(self):
        """Initialize default product catalog."""
        self._products = [
            Product("P001", "Milo", 10.00, "Beverages", 40),
            Product("P002", "Youngs Town Sardines", 26.00, "Food", 50),
            Product("P003", "Bearbrand", 13.00, "Beverages", 45),
            Product("P004", "Kopiko Blanca Twin pack", 16.00, "Beverages", 40),
            Product("P005", "Shampoo", 8.00, "Personal Care", 60),
            Product("P006", "Soap", 25.00, "Personal Care", 33),
            Product("P007", "Lava Cake", 10.00, "Food", 55),
            Product("P008", "Lucky 7 Carne Norte", 27.00, "Food", 150),
            Product("P009", "Freska Tuna", 35.00, "Food", 35),
            Product("P010", "Soft Drink", 15.00, "Beverages", 40),
        ]   

    def get_categories(self) -> List[str]:
              return sorted(list(set(p.category for p in self._products)))

    def get_products(self, search: Optional[str] = None, category: Optional[str] = None) -> List[Product]:
        result = self._products
        if category and category != "All":
            result = [p for p in result if p.category == category]
        if search:
            search_lower = search.lower()
            result = [p for p in result if search_lower in p.name.lower()]
        return result

    def get_cart(self) -> List[CartItem]:
        return self._cart.copy()

    def get_cart_total(self) -> float:
        return sum(item.get_subtotal() for item in self._cart)

    def clear_cart(self):
        self._cart = []

    def get_transactions(self) -> List[Transaction]:
        return self._transactions.copy()

    def get_transaction_by_id(self, trans_id: str) -> Optional[Transaction]:
        return next((t for t in self._transactions if t.id == trans_id), None)


class POSSystem(BasePOS):
    """
    Concrete POS System inheriting from BasePOS.
    Implements all abstract methods with full business logic.
    """

    def add_to_cart(self, product_id: str, quantity: int = 1) -> bool:
        product = next((p for p in self._products if p.id == product_id), None)
        if not product or product.stock < quantity:
            return False

        existing = next((item for item in self._cart if item.product.id == product_id), None)
        if existing:
            new_qty = existing.quantity + quantity
            if product.stock >= new_qty:
                existing.update_quantity(new_qty)
                return True
            return False
        else:
            self._cart.append(CartItem(product, quantity))
            return True

    def update_cart_quantity(self, product_id: str, quantity: int) -> bool:
        item = next((item for item in self._cart if item.product.id == product_id), None)
        if not item:
            return False

        if quantity <= 0:
            self._cart.remove(item)
            return True

        product = next((p for p in self._products if p.id == product_id), None)
        if product and product.stock >= quantity:
            item.update_quantity(quantity)
            return True
        return False

    def remove_from_cart(self, product_id: str) -> bool:
        item = next((item for item in self._cart if item.product.id == product_id), None)
        if item:
            self._cart.remove(item)
            return True
        return False

    def checkout(self, cash_amount: float) -> Optional[Transaction]:
        if not self._cart or cash_amount < self.get_cart_total():
            return None

        # Deduct stock
        for item in self._cart:
            item.product.reduce_stock(item.quantity)

        transaction = Transaction(self._cart, cash_amount)
        self._transactions.append(transaction)
        self._cart = []
        return transaction

    def get_daily_summary(self) -> Dict:
        today = datetime.now().date()
        today_trans = [t for t in self._transactions if t.date.date() == today]
        return {
            "count": len(today_trans),
            "total": sum(t.total for t in today_trans),
            "transactions": today_trans
        }

    def get_all_summary(self) -> Dict:
        return {
            "count": len(self._transactions),
            "total": sum(t.total for t in self._transactions),
            "transactions": self._transactions
        }


class TextReceiptGenerator(ReceiptGenerator):
    """Concrete receipt generator creating text-based receipt output."""

    def generate(self, transaction: Transaction) -> str:
        lines = [
            "=" * 40,
            "SBPOSS STORE",
            "123 Main Street, City",
            "Tel: (123) 456-7890",
            "=" * 40,
            f"Trans ID: {transaction.id}",
            f"Date: {transaction.date.strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 40,
        ]
        for item in transaction.items:
            lines.append(f"{item.product.name:<20} {item.quantity:>3} ₱{item.get_subtotal():>7.2f}")
        lines.extend([
            "-" * 40,
            f"{'Total:':<30} ₱{transaction.total:>7.2f}",
            f"{'Cash:':<30} ₱{transaction.cash_given:>7.2f}",
            f"{'Change:':<30} ₱{transaction.change:>7.2f}",
            "=" * 40,
            "Thank you for your purchase!",
            "Please come again",
        ])
        return "\n".join(lines)


# =============================================================================
# OOP PILLAR 4: POLYMORPHISM - Same interface, different implementations
# =============================================================================

class POSController:
    """
    Polymorphic controller that works with any POSOperations implementation.
    Demonstrates polymorphism by accepting any object that implements POSOperations.
    """

    def __init__(self, pos_system: POSOperations, receipt_generator: ReceiptGenerator):
        self._pos = pos_system
        self._receipt_gen = receipt_generator

    def process_sale(self, product_id: str) -> bool:
        return self._pos.add_to_cart(product_id, 1)

    def complete_checkout(self, cash: float) -> Optional[Transaction]:
        return self._pos.checkout(cash)

    def generate_receipt_text(self, transaction: Transaction) -> str:
        return self._receipt_gen.generate(transaction)

    @property
    def pos(self) -> POSOperations:
        return self._pos


# =============================================================================
# APPLICATION SETUP - Singleton instances for single-user access
# =============================================================================

# Users for authentication. New signups are stored in memory for this app run.
cashier_user = User("cashier", "1001", "Cashier")
users = {
    cashier_user.username: cashier_user
}

# Single POS system instance (single-user design)
pos_system = POSSystem()
receipt_generator = TextReceiptGenerator()
controller = POSController(pos_system, receipt_generator)

# =============================================================================
# FLASK ROUTES
# =============================================================================

@app.route("/")
def index():
    if "logged_in" in session:
        return redirect(url_for("sales"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = users.get(username)
        if user and user.authenticate(username, password):
            session["logged_in"] = True
            session["username"] = user.username
            return redirect(url_for("sales"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/signUp", methods=["GET"])
def sign_up_page():
    return render_template("signUp.html")


@app.route("/signup", methods=["POST"])
def signup():
    full_name = request.form.get("fullname", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not full_name or not username or not password:
        return render_template("signUp.html", error="Please fill in all required fields")

    if password != confirm_password:
        return render_template("signUp.html", error="Passwords do not match")

    if username in users:
        return render_template("signUp.html", error="Username already exists")

    users[username] = User(username, password, full_name)
    return render_template("signUp.html", success="Account created successfully. You can now log in.")


@app.route("/forgotPassword", methods=["GET"])
def forgot_password_page():
    return render_template("forgotPassword.html")


@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    email = request.form.get("email", "").strip()

    if not email:
        return render_template("forgotPassword.html", error="Please enter your email address")

    return render_template(
        "forgotPassword.html",
        success="If the email is registered, password reset instructions will be sent."
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form.get("action")
        product_id = request.form.get("product_id")

        if action == "add":
            controller.process_sale(product_id)
        elif action == "increase":
            item = next((i for i in pos_system.get_cart() if i.product.id == product_id), None)
            if item:
                pos_system.update_cart_quantity(product_id, item.quantity + 1)
        elif action == "decrease":
            item = next((i for i in pos_system.get_cart() if i.product.id == product_id), None)
            if item:
                pos_system.update_cart_quantity(product_id, item.quantity - 1)
        elif action == "remove":
            pos_system.remove_from_cart(product_id)

        return redirect(url_for("sales", **{k: v for k, v in request.args.items()}))

    search = request.args.get("search", "")
    category = request.args.get("category", "")
    products = pos_system.get_products(search=search, category=category)
    categories = pos_system.get_categories()
    cart = pos_system.get_cart()
    total = pos_system.get_cart_total()

    return render_template(
        "sales.html",
        products=products,
        categories=categories,
        cart=cart,
        total=total,
        search=search,
        category=category
    )


@app.route("/payment", methods=["GET", "POST"])
def payment():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    total = pos_system.get_cart_total()
    if total == 0:
        return redirect(url_for("sales"))

    if "payment_input" not in session:
        session["payment_input"] = ""

    error = None
    change = None

    if request.method == "POST":
        action = request.form.get("action")
        digit = request.form.get("digit")

        if digit is not None:
            current = session.get("payment_input", "")
            if digit == "C":
                session["payment_input"] = ""
            elif digit == ".":
                if "." not in current:
                    session["payment_input"] = current + digit
            else:
                session["payment_input"] = current + digit
            session.modified = True

        elif action == "confirm":
            current = session.get("payment_input", "")
            try:
                cash = float(current) if current else 0.0
                if cash < total:
                    error = f"Payment insufficient. Need ₱{total:.2f}"
                    change = cash - total
                else:
                    transaction = controller.complete_checkout(cash)
                    if transaction:
                        session.pop("payment_input", None)
                        return redirect(url_for("receipt", trans_id=transaction.id))
                    else:
                        error = "Checkout failed"
            except ValueError:
                error = "Invalid amount"

    current_input = session.get("payment_input", "")
    if current_input:
        try:
            cash_val = float(current_input)
            change = cash_val - total
        except ValueError:
            change = None

    return render_template(
        "payment.html",
        total=total,
        current_input=current_input if current_input else "0.00",
        change=change,
        error=error
    )


@app.route("/receipt/<trans_id>")
def receipt(trans_id):
    if "logged_in" not in session:
        return redirect(url_for("login"))

    transaction = pos_system.get_transaction_by_id(trans_id)
    if not transaction:
        return redirect(url_for("sales"))

    return render_template("receipt.html", transaction=transaction)


@app.route("/summary")
def summary():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    search_id = request.args.get("search_id", "")
    daily = pos_system.get_daily_summary()
    all_summary = pos_system.get_all_summary()

    if search_id:
        transactions = [t for t in all_summary["transactions"] if search_id.upper() in t.id]
    else:
        transactions = all_summary["transactions"]

    return render_template(
        "summary.html",
        transactions=transactions,
        today_total=daily["total"],
        today_count=daily["count"],
        all_total=all_summary["total"],
        search_id=search_id
    )

# For Vercel deployment
if __name__ == "__main__":
    app.run(debug=True)
