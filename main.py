import csv
import os
from datetime import datetime

# ---------------------- Global Variables ----------------------

expenses = []
budget = 0.0
CSV_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

# ---------------------- File Handling ----------------------

def load_expenses():
    """Load expenses from CSV file."""
    global expenses
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append({
                        'date': row['date'],
                        'category': row['category'],
                        'amount': float(row['amount']),
                        'description': row['description']
                    })
                except (ValueError, KeyError):
                    print(" Skipping invalid CSV entry.")

def save_expenses():
    """Save expenses to CSV file."""
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for exp in expenses:
            writer.writerow(exp)
    print(" Expenses saved to file.")

def load_budget():
    """Load budget from text file."""
    global budget
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, 'r') as file:
                budget = float(file.read().strip())
        except ValueError:
            budget = 0.0

def save_budget():
    """Save budget to text file."""
    with open(BUDGET_FILE, 'w') as file:
        file.write(str(budget))

# ---------------------- Expense & Budget Management ----------------------

def add_expense():
    """Add a new expense and show remaining budget."""
    global budget
    try:
        date = input("Enter date (YYYY-MM-DD): ")
        datetime.strptime(date, '%Y-%m-%d')  # Validate date
        category = input("Enter category (e.g., Food, Travel): ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")

        expense = {
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        }
        expenses.append(expense)
        print(" Expense added successfully.")

        # Show remaining balance
        if budget > 0:
            total_spent = sum(exp['amount'] for exp in expenses)
            remaining = budget - total_spent
            if remaining < 0:
                print(f" Over Budget! You've exceeded by ₹{abs(remaining):.2f}.")
            else:
                print(f" Remaining balance: ₹{remaining:.2f} of ₹{budget:.2f}")

    except ValueError:
        print(" Invalid input. Please try again.")

def view_expenses():
    """Display all stored expenses."""
    if not expenses:
        print(" No expenses recorded yet.")
        return
    print("\n Expense List:")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. Date: {exp['date']}, Category: {exp['category']}, "
              f"Amount: ₹{exp['amount']:.2f}, Description: {exp['description']}")

def set_budget():
    """Set or update the monthly budget."""
    global budget
    try:
        budget = float(input("Enter your monthly budget (₹): "))
        save_budget()
        print(f" Budget set to ₹{budget:.2f}")
    except ValueError:
        print(" Invalid input. Please enter a numeric value.")

def track_budget():
    """Check current total against budget and show status."""
    if budget <= 0:
        print("⚠️ No budget set. Use option 3 to set a monthly budget.")
        return

    total_spent = sum(exp['amount'] for exp in expenses)
    print(f"\n💰 Total spent so far: ₹{total_spent:.2f}")

    if total_spent > budget:
        print(f" You have exceeded your ₹{budget:.2f} budget by ₹{total_spent - budget:.2f}")
    else:
        print(f" You have ₹{budget - total_spent:.2f} remaining from your ₹{budget:.2f} budget.")

# ---------------------- Interactive Menu ----------------------

def menu():
    """Display the main interactive menu."""
    load_expenses()
    load_budget()

    while True:
        print("\n========== Personal Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Set Budget")
        print("4. Track Budget")
        print("5. Save Expenses")
        print("6. Exit")
        choice = input("Choose an option (1–6): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            set_budget()
        elif choice == '4':
            track_budget()
        elif choice == '5':
            save_expenses()
        elif choice == '6':
            save_expenses()
            save_budget()
            print(" Exiting... Your data has been saved.")
            break
        else:
            print(" Invalid choice. Please enter a number between 1 and 6.")

# ---------------------- Program Entry ----------------------

if __name__ == "__main__":
    menu()
