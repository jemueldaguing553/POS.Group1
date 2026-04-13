Group1 BSCS 1A
-Jemuel Daguing
-Denis Guibao
-Joshua Simbajon
-Angel Paquibot

 
Title & Description

Tindahan Ni Maricel POS System is a simple web-based Point of Sale system developed using HTML, CSS, JavaScript, and Python Flask.
It allows user authentication through a login module and performs basic sales transactions using a cash payment system.

---

 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.x
- Flask
- Git (for cloning repository)
- Web browser (Chrome, Edge, etc.)

Install Flask using:

pip install flask

---

 Installation

1. Clone the repository from GitHub:

2. Navigate to the project folder:

cd pos-system

3. Run the Flask application:

python app.py

---

 Usage

 Login Module

1. Open the system in browser
2. Enter the User ID:

1001

3. Click Login
4. If valid, user is redirected to the POS page

---

 Cash Payment Module

1. Add items to the cart
2. Enter the cash amount
3. System calculates:
   - Total price
   - Change
4. Click Proceed to complete transaction

Example:

Total: 100
Cash: 150
Change: 50

---

 Module Description

 Module 1: Login Module

The Login Module handles user authentication before accessing the POS system.

Features:

- Accepts User ID input
- Validates user using predefined credentials
- Uses Flask backend for routing
- Stores login session (via localStorage or Flask session)
- Redirects to POS page after successful login
- Blocks unauthorized access

Functionality:

- Input validation
- Conditional checking ("if-else")
- Page redirection
- Session handling

Rules:

- User must enter correct User ID ("1001")
- Empty input is not allowed
- Unauthorized users cannot access POS page

---

Module 2: Cash Payment Module

The Cash Payment Module manages the transaction process and payment computation.

Features:

- Displays selected items and total price
- Accepts cash input from user
- Automatically calculates change
- Validates sufficient payment
- Confirms successful transaction

Functionality:

- Arithmetic operations (total and change)
- Event handling ("oninput", button click)
- Conditional logic for payment validation
- Dynamic UI updates

Rules:

- Cash must be greater than or equal to total
- If cash is insufficient, transaction is denied
- After successful transaction, cart resets

---
