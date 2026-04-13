from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

VALID_USER = "1001"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("userID")

        if user_id == VALID_USER:
            session["logged_in"] = True
            return redirect("/pos")
        else:
            return render_template("login.html", error="Invalid User ID")

    return render_template("login.html")


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
#chatgpt

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/page2")
def page2():
    return render_template("page2.html")

if __name__ == "__main__":
    app.run(debug=True)