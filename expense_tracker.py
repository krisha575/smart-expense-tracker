import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Please enter a valid number for amount.")
        return

    category = input("Enter category (Food/Travel/Study/etc): ").strip()
    if category == "":
        print("Category cannot be empty.")
        return

    description = input("Enter description: ").strip()
    if description == "":
        print("Description cannot be empty.")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])

    print("Expense added successfully.")


def view_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            print("\nDate       | Amount | Category | Description")
            print("-" * 50)
            for row in reader:
                print(f"{row[0]:10} | {row[1]:6} | {row[2]:8} | {row[3]}")
    except FileNotFoundError:
        print("No expenses found.")


def total_expense():
    total = 0
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                total += float(row[1])
        print(f"\nTotal Expense: ₹{total}")
    except FileNotFoundError:
        print("No expenses found.")


def category_summary():
    summary = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[2]
                amount = float(row[1])
                summary[category] = summary.get(category, 0) + amount

        print("\nCategory-wise Summary")
        print("-" * 30)
        for cat, amt in summary.items():
            print(f"{cat}: ₹{amt}")

    except FileNotFoundError:
        print("No expenses found.")


def monthly_summary():
    monthly_data = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                date = row[0]
                amount = float(row[1])
                month = date[:7]  # YYYY-MM

                monthly_data[month] = monthly_data.get(month, 0) + amount

        print("\nMonthly Expense Summary")
        print("-" * 30)
        for month, total in sorted(monthly_data.items()):
            print(f"{month}: ₹{total}")

    except FileNotFoundError:
        print("No expenses found.")


def filter_by_month():
    month_input = input("Enter month (YYYY-MM): ").strip()

    if len(month_input) != 7 or month_input[4] != "-":
        print("Invalid format. Use YYYY-MM.")
        return

    found = False
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            print("\nDate       | Amount | Category | Description")
            print("-" * 50)

            for row in reader:
                if row[0].startswith(month_input):
                    print(f"{row[0]:10} | {row[1]:6} | {row[2]:8} | {row[3]}")
                    found = True

        if not found:
            print("No expenses found for this month.")

    except FileNotFoundError:
        print("No expenses found.")


def main_menu():
    while True:
        print("\n==== SMART PERSONAL EXPENSE TRACKER ====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Total Expense")
        print("4. Category-wise Summary")
        print("5. Monthly Expense Summary")
        print("6. View Expenses by Month")
        print("7. Exit")

        choice = input("Choose option (1-7): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            filter_by_month()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


main_menu()
