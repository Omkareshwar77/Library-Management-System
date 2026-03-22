from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
FILE = "library.txt"

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    books = load_data()
    return render_template("index.html", books=books)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    author = request.form["author"]

    books = load_data()
    books.append({"name": name, "author": author, "issued": False})
    save_data(books)

    return redirect("/")

@app.route("/issue/<int:id>")
def issue(id):
    books = load_data()
    if not books[id]["issued"]:
        books[id]["issued"] = True
        save_data(books)
    return redirect("/")

@app.route("/return/<int:id>")
def return_book(id):
    books = load_data()
    if books[id]["issued"]:
        books[id]["issued"] = False
        save_data(books)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    books = load_data()
    if 0 <= id < len(books):
        books.pop(id)
        save_data(books)
    return redirect("/")
    
app.run(debug=True)