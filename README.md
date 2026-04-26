## Group1 BSCS 1A

- Angel Paquibot

- Denis Martin Guibao

- Jemuel Daguing

- Joshua Simbajon

---
 
# Title & Description

# SBPOSS Small Bussiness Point of Sale System
  
is a simple web-based Point of Sale system developed using HTML, CSS, JavaScript, and Python Flask.
It allows user authentication through a login module and performs basic sales transactions using a cash payment system.

---

# Module Description

# MODULE 1: SALES TRANSACTION

This module is the main sales system of the POS (Point-of-Sale). It allows the user to add products to a cart, manage quantities, and calculate the total amount of the purchase.

 ## Features

- Displays list of products with prices

- Search bar to find products easily

- Category buttons to filter products

- Add products to cart

- Increase or decrease quantity of items

- Remove items from cart

- Automatically calculates total price

- Checkout button to complete the sale

## How it works

- The system shows all available products.

- The user can search or choose a category to find items.

- Clicking Add puts the product into the cart.

- The user can increase, decrease, or remove items in the cart.

- The system automatically updates the total price.

- When the user clicks Proceed Checkout, the system confirms the sale.

- After checkout, the cart is cleared and ready for a new transaction.

## Usage

- Used by the cashier to process customer purchases

- Helps organize products and prices in one system

- Makes selling faster and easier

- Used in small stores or school POS projects

## Notes

- If the cart is empty, checkout will not proceed

- Quantity cannot go below zero

- All prices are automatically calculated by the system

- Search helps quickly find products

- Category buttons help filter items

- This module works offline using only the browser

---

# MODULE 2: CASH PAYMENT

This module is a simple cash payment system used in a Point-of-Sale (POS) application. It allows the cashier to enter the amount of cash received from the customer, automatically calculates the change, and confirms the payment.

## Features

- Displays the total amount to be paid

- Allows input of cash using a keypad

- Automatically calculates change

- Shows warning if payment is not enough

- Confirm button to complete the payment

- Cancel button to clear input

- Simple navigation back to sales page

## How it works

- The system shows the total amount that needs to be paid.

- The cashier enters the cash amount using the on-screen keypad.

- The system automatically checks the entered amount.

- It calculates the change (if any).

- If the cash is enough, the payment can be confirmed.

- If the cash is not enough, an error message will appear.

- After confirmation, the system shows a success message and returns to the sales page.

## Usage

- Used by the cashier during checkout

- Helps in quick and correct cash transactions

- Prevents mistakes in change calculation

- Used in small retail stores or school POS projects

## Notes
  
- The system only accepts cash payments (no card or online payments

- Input is done using buttons, not keyboard typing

- Payment must be equal or higher than total amount

- If cancelled, all input will be cleared

- This is designed for simple and offline use

---

# MODULE 3: RECEIPT

- This module displays the final transaction details after a successful payment. It shows a complete summary of purchased items, total amount, cash received, and change, similar to a printed receipt.

## Features

- Displays store information (name, address, contact)

- Shows list of purchased items with quantity and price

- Displays total amount, cash given, and change

- Automatically saves transaction to sales history

- Provides navigation buttons (Sales, Payment, Summary)

- Clears cart after transaction is completed

## How it works

- The system retrieves the latest transaction from storage.

- If no transaction is found, the user is redirected to the Sales page.

- The system displays all purchased items in a table format.

- It calculates and shows the total, cash, and change.

- The transaction is saved to the sales history list.

- When the user clicks OK, the system clears the cart and resets for the next transaction.

## Usage

- Used after completing a payment

- Allows cashier to review the transaction

- Acts as a digital receipt for the customer

- Records sales for tracking and summary

## Notes

- If no transaction exists, the page will redirect to Sales

- All data is stored using localStorage (browser-based)

- Receipt is not printable by default

- Data can be cleared if browser storage is reset

- Used for basic POS systems and school projects

---

# MODULE 4: DAILY SALES SUMMARY

- This module displays the record of all completed transactions. It allows the user to view sales history, search transactions, and monitor daily sales performance.

## Features

- Displays list of all sales transactions

- Shows transaction ID, date, items, and total amount

- Search bar to find transactions by ID

- Automatically calculates total sales

- Displays number of transactions for the current day

- Shows total sales for today

- Scrollable table for viewing many records

## How it works

- The system retrieves all saved sales data from storage.

- Each transaction is assigned a unique ID.

- The system displays all transactions in a table format.

- The user can search for a transaction using the ID.

- The system calculates the grand total of all sales.

- It checks which transactions were made today.

- The system counts today's transactions and calculates today's total sales.

- All data is updated dynamically on the page.

## Usage

- Used by the cashier or admin to review past transactions

- Helps track daily sales performance

- Useful for monitoring income and activity

- Used for reports in small stores or school POS systems

## Notes

- All data is stored using localStorage (browser-based)

- Clearing browser data will erase all sales history

- Transaction IDs are automatically generated

- Search works only by transaction ID

- Date is based on the system's local time

- This module works offline without a database

---
