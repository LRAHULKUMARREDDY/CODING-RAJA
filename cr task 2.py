#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3
from tabulate import tabulate  # Install using: pip install tabulate
from datetime import datetime

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    # Create transactions table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            type TEXT,
            amount REAL,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function to record a transaction
def record_transaction(category, transaction_type, amount):
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO transactions (category, type, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (category, transaction_type, amount, date))

    conn.commit()
    conn.close()

# Function to calculate remaining budget
def calculate_budget():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    # Calculate total income
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE type="Income"')
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE type="Expense"')
    total_expenses = cursor.fetchone()[0] or 0

    conn.close()

    remaining_budget = total_income - total_expenses
    return remaining_budget

# Function to analyze expenses by category
def analyze_expenses():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    # Get expenses by category
    cursor.execute('SELECT category, SUM(amount) FROM transactions WHERE type="Expense" GROUP BY category')
    expense_categories = cursor.fetchall()

    conn.close()

    # Display expense analysis
    print("\nExpense Analysis:")
    if not expense_categories:
        print("No expenses recorded.")
    else:
        headers = ["Category", "Total Amount"]
        print(tabulate(expense_categories, headers=headers, tablefmt="fancy_grid"))

# Function to display all transactions
def display_transactions():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    # Get all transactions
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    conn.close()

    # Display all transactions
    print("\nAll Transactions:")
    if not transactions:
        print("No transactions recorded.")
    else:
        headers = ["ID", "Category", "Type", "Amount", "Date"]
        print(tabulate(transactions, headers=headers, tablefmt="fancy_grid"))

# Main function to interact with the user
def main():
    initialize_database()

    while True:
        print("\n1. Record Income\n2. Record Expense\n3. View Remaining Budget\n4. Analyze Expenses\n5. View All Transactions\n6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            category = input("Enter income category: ")
            amount = float(input("Enter income amount: "))
            record_transaction(category, "Income", amount)

        elif choice == '2':
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            record_transaction(category, "Expense", amount)

        elif choice == '3':
            remaining_budget = calculate_budget()
            print(f"\nRemaining Budget: ${remaining_budget:.2f}")

        elif choice == '4':
            analyze_expenses()

        elif choice == '5':
            display_transactions()

        elif choice == '6':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()

