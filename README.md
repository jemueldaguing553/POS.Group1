from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

VALID_USER = "1001"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    user_id = request.form.get("userID")

    if user_id == VALID_USER:
        session["logged_in"] = True
        return redirect("/pos")
    else:
        return render_template("login.html", error="Invalid User ID")

@app.route("/pos")
def pos():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("pos.html")

@app.route("/receipt")
def receipt():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("receipt.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
