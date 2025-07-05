import csv
import os
from datetime import datetime

expenses = []
budget = 0.0
CSV_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

# ------------------------ File Operations ------------------------

def load_expenses():
    """Load expenses from CSV file if it exists."""
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
                    print("⚠️ Skipping invalid entry in CSV.")

def save_expenses():
    """Save current expenses to CSV file."""
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for exp in expenses:
            writer.writerow(exp)
    print(" Expenses saved to file.")

def load_budget():
    """Load the budget value from a text file."""
    global budget
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, 'r') as file:
                budget = float(file.read().strip())
        except ValueError:
            budget = 0.0

def save_budget():
    """Save the budget value to a text file."""
    with open(BUDGET_FILE, 'w') as file:
        file.write(str(budget))

# ------------------------ Expense Management ------------------------

def add_expense():
    """Prompt user to add an expense and store it."""
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
        print(" Expense added.")
    except ValueError:
        print(" Invalid input. Please try again.")

def view_expenses():
    """Display all stored expenses."""
    if not expenses:
        print(" No expenses to display.")
        return
    print("\n📋 Expense List:")
    for i, exp in enumerate(expenses, start=1):
        try:
            print(f"{i}. Date: {exp['date']}, Category: {exp['category']}, "
                  f"Amount: ₹{exp['amount']:.2f}, Description: {exp['description']}")
        except KeyError:
            print(f"{i}. ⚠️ Invalid entry found, skipping.")

def set_budget():
    """Allow user to input and save a monthly budget."""
    global budget
    try:
        budget = float(input("Enter your monthly budget amount: ₹"))
        save_budget()
        print(f" Budget set to ₹{budget:.2f}")
    except ValueError:
        print(" Invalid input. Please enter a numeric value.")

def track_budget():
    """Compare current expenses against the set budget."""
    if budget <= 0:
        print("⚠️ No budget set. Please set your monthly budget first.")
        return
    total_spent = sum(exp['amount'] for exp in expenses)
    print(f"\n Total spent: ₹{total_spent:.2f}")
    if total_spent > budget:
        print(" You have exceeded your budget!")
    else:
        remaining = budget - total_spent
        print(f" You have ₹{remaining:.2f} left for the month.")

# ------------------------ Interactive Menu ------------------------

def menu():
    """Main interactive menu."""
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
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice. Please select a valid option.")

# ------------------------ Program Entry Point ------------------------

if __name__ == "__main__":
    menu()
1