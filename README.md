
---

# POS Group 1 - Small Business Point of Sale System

BSCS 1A Group 1
Members
Angel Paquibot
Guibao
Daguing
Simbajon

The Small Business Point of Sale System is a web-based application designed to handle sales transactions, process customer payments, generate receipts, and track daily sales performance.

It provides a simple and efficient interface for cashiers to manage products, handle customer purchases, and monitor business activity in real time.

## Module 1: Sales Transaction 
### Features
- Display available products with:
- Product name
- Price
- Stock quantity
- Search products by name
- Filter products by category
- Add items to cart
   - Adjust cart items:
   - Increase quantity
   - Decrease quantity
   - Remove item
- Real-time cart total calculation
- Proceed to checkout

### Sales Management
- Interactive product grid layout
- Category-based filtering system
- Shopping cart preview panel
- Automatic total price computation
- Prevent checkout when cart is empty

## Module 2: Cash Payment (payment.html)
### Features
- Displays total purchase amount
- Numeric keypad for cash input
- Real-time input display
- Automatic change calculation
- Error handling for insufficient payment
- Confirm payment process

### Payment Processing
- Cash-only transaction system
- Dynamic calculation:
- Cash received
   - Change amount
   - Clear/reset input option
- Validation before confirming payment

## Module 3: Receipt Generation (receipt.html)
### Features
- Generates printable receipt
- Displays:
   - Store information
   - Transaction ID
   - Date and time
   - List of purchased items
- Shows:
   - Item quantity
   - Price per item
   - Subtotal per item
- Displays totals:
   - Total amount
   - Cash received
   - Change

### Receipt Details
- Clean receipt-style layout
- Auto-generated transaction record
- Navigation options:
   - New Sale
   - Daily Summary

## Module 4: Daily Sales Summary (summary.html)
### Features
- Displays daily sales statistics:
   - Total sales today
   - Number of transactions
   - All-time sales
   - Search transactions by ID
   - Tabular transaction history
   - Reporting System
   - View all completed transactions
- Displays:
   - Transaction ID
   - Date and time
   - Number of items
   - Total amount
   - Real-time sales tracking

## System Workflow
### 1.Sales Transaction
- User selects products and adds them to cart
### 2.Checkout 
- User proceeds to payment page 
### 3.Payment
- Cash is entered and validated
- Change is calculated
### 4.Receipt
- Transaction is finalized
- Receipt is generated
### 5.Summary
- Transaction is recorded in daily summary

## Technology Stack
- Backend: Python Flask
- Frontend: HTML, CSS (Responsive Design)
- Data Storage: JSON-based storage (products, transactions)
- Session Management: Flask sessions
- Architecture: Modular template-based system

## Installation and Setup
### Prerequisites
Python 3.x
Flask installed
### Installation Steps
1.Prepare project files
2.Install Flask:
   pip install flask
3.Run the application:
   python app.py
4.Open browser:
   http://localhost:5000

## Usage
### 1.Sales Process
- Open Sales page
- Select or search products
- Add items to cart
- Click Proceed Checkout

### 2.Payment Process
- Enter customer cash using keypad
- Check computed change
- Click Confirm Payment

### 3.Receipt
- View transaction receipt
- Print if needed
- Start new sale or go to summary

### 4.Daily Summary
- View all transactions
- Monitor daily and total sales
- Search transactions by ID

## Key Features Summary
- Simple and user-friendly POS interface
- Real-time cart and payment calculation
- Automatic receipt generation
- Sales tracking and reporting
- Modular system design