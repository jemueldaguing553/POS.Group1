<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(to right, #1e3c72, #2a5298);
}

.container {
    max-width: 1000px;
    margin: 40px auto;
    background: #f5f5f5;
    border-radius: 15px;
    padding: 20px;
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.left { 
    flex: 3;
    min-width: 300px; 
}
.right {
    flex: 2;
    background: white;
    padding: 15px;
    border-radius: 10px;
    min-width: 250px; 
}

input {
    width: 100%;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
    box-sizing: border-box; 
}

.categories button {
    margin: 3px;
    padding: 6px 12px;
    border-radius: 10px;
    border: none;
    background: #ddd;
    cursor: pointer;
}

.categories .active {
    background: #4a90e2;
    color: white;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    text-align: left;
    padding: 8px;
    border-bottom: 2px solid #ccc;
}

td {
    padding: 8px;
    border-bottom: 1px solid #ddd;
}

.add-btn {
    background: #4a90e2;
    color: white;
    padding: 5px 10px;
    border-radius: 8px;
    border: none;
}

.proceed-btn {
    width: 100%;
    padding: 12px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 10px;
    margin-top: 10px;
}

.checkout-box {
    height: 200px;
    overflow-y: auto;
}

@media screen and (max-width: 800px) {
    .container {
        flex-direction: column; /* stack left and right vertically */
    }
    .left, .right {
        width: 100%;
    }
}
</style>
</head>

<body>

<div class="container">

<div class="left">
    <h2>Tindahan Ni Maricel</h2>

    <input type="text" id="search" placeholder="Search product..." onkeyup="renderProducts()">

    <div class="categories" id="categoryButtons">
        <button onclick="filterCategory('All')" class="active">All</button>
        <button onclick="filterCategory('Groceries')">Groceries</button>
        <button onclick="filterCategory('Beverages')">Beverages</button>
        <button onclick="filterCategory('Snacks')">Snacks</button>
        <button onclick="filterCategory('Household')">Household</button>
    </div>

    <table id="productTable">
        <thead>
            <tr>
                <th>Item</th>
                <th>Category</th>
                <th>Price</th>
                <th>Add</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>
</div>

<div class="right">
    <h3>Checkout</h3>

    <div class="checkout-box">
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Qty</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody id="cart"></tbody>
        </table>
    </div>

    <p><strong>Total:</strong> ₱<span id="total">0</span></p>

    <p><strong>Cash:</strong></p>
    <input type="number" id="cash" oninput="calculateChange()">

    <p><strong>Change:</strong> ₱<span id="change">0</span></p>

    <button class="proceed-btn" onclick="checkout()">Proceed</button>
</div>

</div>

<script>

if (!localStorage.getItem("loggedIn")) {
    window.location.href = "/";
}

localStorage.removeItem("cart");

const products = [
    {name: "Rice", price: 45, category: "Groceries"},
    {name: "Soft Drinks", price: 18, category: "Beverages"},
    {name: "Canned Sardines", price: 20, category: "Groceries"},
    {name: "Chips", price: 15, category: "Snacks"},
    {name: "Detergent", price: 25, category: "Household"}
];

let selectedCategory = "All";
let cart = {};

function renderProducts() {
    let table = document.querySelector("#productTable tbody");
    let search = document.getElementById("search").value.toLowerCase();

    table.innerHTML = "";

    products.forEach(p => {
        if ((selectedCategory === "All" || p.category === selectedCategory) &&
            p.name.toLowerCase().includes(search)) {

            table.innerHTML += `
            <tr>
                <td>${p.name}</td>
                <td>${p.category}</td>
                <td>₱${p.price}</td>
                <td><button class="add-btn" onclick="addItem('${p.name}')">Add</button></td>
            </tr>`;
        }
    });
}

function filterCategory(category) {
    selectedCategory = category;

    document.querySelectorAll("#categoryButtons button").forEach(btn => {
        btn.classList.remove("active");
        if (btn.innerText === category) btn.classList.add("active");
    });

    renderProducts();
}

function addItem(name) {
    let product = products.find(p => p.name === name);

    if (!cart[name]) cart[name] = {qty: 1, price: product.price};
    else cart[name].qty++;

    displayCart();
}

function displayCart() {
    let cartTable = document.getElementById("cart");
    cartTable.innerHTML = "";

    let total = 0;

    for (let item in cart) {
        let data = cart[item];
        let subtotal = data.qty * data.price;
        total +
