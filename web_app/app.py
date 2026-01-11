from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "expenses.csv"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADD EXPENSE ----------------
@app.route("/add", methods=["POST"])
def add_expense():
    amount = request.form["amount"]
    category = request.form["category"].strip().title()  # NORMALIZED
    description = request.form["description"]

    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])

    return "Expense added successfully! <br><br><a href='/'>Go Back</a>"



# ---------------- MONTHLY SUMMARY ----------------
@app.route("/monthly")
def monthly_summary():
    summary = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                month = row[0][:7]  # YYYY-MM
                amount = float(row[1])
                summary[month] = summary.get(month, 0) + amount
    except FileNotFoundError:
        pass

    return render_template("monthly.html", summary=summary)


# ---------------- CATEGORY SUMMARY ----------------
@app.route("/category")
def category_summary():
    summary = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[2]
                amount = float(row[1])
                summary[category] = summary.get(category, 0) + amount
    except FileNotFoundError:
        pass

    return render_template("category.html", summary=summary)


# ---------------- CHARTS ----------------
@app.route("/charts")
def charts():
    category_data = {}
    monthly_data = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                date = row[0]
                amount = float(row[1])
                category = row[2]

                # Category-wise
                category_data[category] = category_data.get(category, 0) + amount

                # Monthly-wise
                month = date[:7]
                monthly_data[month] = monthly_data.get(month, 0) + amount
    except FileNotFoundError:
        pass

    return render_template(
        "charts.html",
        category_data=category_data,
        monthly_data=monthly_data
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
