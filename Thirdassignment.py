from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient


class Expense:
    def __init__(self, description, amount, date):
        self.description = description
        self.amount = amount
        self.date = date

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "date": self.date
        }

class ExpenseTracker:
    def __init__(self):
        self.client = MongoClient("localhost",27017)
        self.db = self.client["ExpenseDB"]
        self.collection = self.db["expenses"]

    # connection = pymongo.MongoClient("localhost", 27017)
    # database = connection["ExpenseDB"]
    # collection = database["expenses"]

    def add_expense(self):
        description :str= input("Enter description: ")
        try:
            amount:float = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount.")
            return

        date:str = input("Enter date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")  # Validate date
        except ValueError:
            print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")
            return
        expense = {
            "description": description,
            "amount": amount,
            "date": date
        }

        self.collection.insert_one(expense)
        print("Expense added successfully!")




    def view_expenses(self):
        expenses = self.collection.find()
        print("\n--- All Expenses ---")
        for exp in expenses:
            print(f"ID: {exp['_id']}, Description: {exp['description']}, Amount: {exp['amount']}, Date: {exp['date']}")
        print()



    def view_total_expense(self):
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
        result = list(self.collection.aggregate(pipeline))
        total = result[0]["total"] if result else 0
        print(f"\nTotal Expenses: {total}\n")

    def delete_expense(self):
        expense_id = input("Enter ID of expense to delete: ")
        try:
            result = self.collection.delete_one({"_id": ObjectId(expense_id)})
            if result.deleted_count:
                print("Expense deleted successfully.\n")
            else:
                print("No expense found with the given ID.\n")
        except:
            print("Invalid ID format.\n")

    def menu(self):
        while True:
            print("Personal Expense Tracker")
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. View Total Expenses")
            print("4. Delete an Expense")
            print("5. Exit")
            choice = input("Enter your option: ")

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.view_total_expense()
            elif choice == '4':
                self.delete_expense()
            elif choice == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option. Try again.\n")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.menu()
