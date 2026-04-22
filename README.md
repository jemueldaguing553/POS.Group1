Group1 BSCS 1A

-Angel Paquibot

-Denis Martin Guibao

-Jemuel Daguing

-Joshua Simbajon

---
 
--- Title & Description

--- SBPOSS Small Bussiness Point of Sale System
  
is a simple web-based Point of Sale system developed using HTML, CSS, JavaScript, and Python Flask.
It allows user authentication through a login module and performs basic sales transactions using a cash payment system.

---

--- Module Description

--- MODULE 1: SALES TRANSACTION

This module is the main sales system of the POS (Point-of-Sale). It allows the user to add products to a cart, manage quantities, and calculate the total amount of the purchase.

-- Features

- Displays list of products with prices

- Search bar to find products easily

- Category buttons to filter products

- Add products to cart

- Increase or decrease quantity of items

- Remove items from cart

- Automatically calculates total price

- Checkout button to complete the sale

-- How it works

- The system shows all available products.

- The user can search or choose a category to find items.

- Clicking Add puts the product into the cart.

- The user can increase, decrease, or remove items in the cart.

- The system automatically updates the total price.

- When the user clicks Proceed Checkout, the system confirms the sale.

- After checkout, the cart is cleared and ready for a new transaction.

-- Usage

- Used by the cashier to process customer purchases

- Helps organize products and prices in one system

- Makes selling faster and easier

- Used in small stores or school POS projects

-- Notes

- If the cart is empty, checkout will not proceed

- Quantity cannot go below zero

- All prices are automatically calculated by the system

- Search helps quickly find products

- Category buttons help filter items

- This module works offline using only the browser

---

--- MODULE 2: CASH PAYMENT

This module is a simple cash payment system used in a Point-of-Sale (POS) application. It allows the cashier to enter the amount of cash received from the customer, automatically calculates the change, and confirms the payment.

-- Features

- Displays the total amount to be paid

- Allows input of cash using a keypad

- Automatically calculates change

- Shows warning if payment is not enough

- Confirm button to complete the payment

- Cancel button to clear input

- Simple navigation back to sales page

-- How it works

- The system shows the total amount that needs to be paid.

- The cashier enters the cash amount using the on-screen keypad.

- The system automatically checks the entered amount.

- It calculates the change (if any).

- If the cash is enough, the payment can be confirmed.

- If the cash is not enough, an error message will appear.

- After confirmation, the system shows a success message and returns to the sales page.

-- Usage

- Used by the cashier during checkout

- Helps in quick and correct cash transactions

- Prevents mistakes in change calculation

- Used in small retail stores or school POS projects

-- Notes
  
- The system only accepts cash payments (no card or online payments

- Input is done using buttons, not keyboard typing

- Payment must be equal or higher than total amount

- If cancelled, all input will be cleared

- This is designed for simple and offline use

---
