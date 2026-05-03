# Day - 23

def save_data(contacts, expenses):
    import json
    import os
    import shutil
    if os.path.exists("data.json"):
        shutil.copy("data.json" , "data_backup.json")

    with open("data.json", "w") as file:
        json.dump({
            "contacts": contacts,
            "expenses": expenses
        }, file)


def load_data():
    import json
    import os
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data.get("contacts", {}), data.get("expenses", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print("No saved data found. Starting fresh.")

        if os.path.exists("data_backup.json"):
            with open("data_backup.json", "r") as file:
                data = json.load(file)
                print("✔ Backup restored!")
                return data.get("contacts", {}), data.get("expenses", {})
        print("⚠  No backup found. Starting Fresh.")
        return {}, {}


def contact_manager(contacts, expenses):
    while True:
        print("\n---- Contact Manager ----")
        print("\n1 Add new contact")
        print("2 Search contact")
        print("3 Update contact")
        print("4 Delete contact")
        print("5 Show All contact")
        print("6 Exit")
        try:
            choice = int(input("Enter choice : "))
        except ValueError:
            print("Invalid choice. Please try again.")
            continue

        if choice == 1:
            name = input("Enter a name : ").strip().title()
            phone = input("Enter a phone number : ").strip()
            if name in contacts:
                print("Contact already exists. Updating number.")
            else:
                print("Contact added successfully.")
            contacts[name] = phone
            save_data(contacts, expenses)
        elif choice == 2:
            query = input("Enter name to search : ").strip().lower()
            found = False
            for name, phone in contacts.items():
                if query in name.lower():
                    print(f"{name}: {phone}")
                    found = True
            if not found:
                 print("No matching contacts found.")
        elif choice == 3:
            name = input("Enter a name to update : ").strip().title()
            if name in contacts:
                phone = input("Enter a phone number : ").strip()
                contacts[name] = phone
                print("Contact updated successfully.")
                save_data(contacts, expenses)
            else:
                print("Contact not found.")
        elif choice == 4:
            name = input("Enter a name to delete : ").strip().title()
            if name in contacts:
                confirm = input("Are you sure? (y/n):")
                if confirm.lower() == "y":
                    del contacts[name]
                    print("Contact deleted successfully.")
                    save_data(contacts, expenses)

            else:
                print("Contact not found.")
        elif choice == 5:
            print("\nAll contacts:")
            for name, phone in contacts.items():
                print(f"{name} : {phone}")
        elif choice == 6:
            print("Exiting contact Book. Goodbye!")
            break
        else:
            print("Invalid choice.Please try again.")



def expense_manager(expenses, contacts):
    while True:
        print("\n---- Expense Manager ----")
        print("1. Add Expense")
        print("2. Show Expenses")
        print("3. Summary")
        print("4. Back")

        choice = input("Enter your choice : ").strip()

        if choice == "1":
            category = input("Enter category : ").strip().title()
            amount = float(input("Enter amount : "))
            expenses[category] = amount
            save_data(contacts, expenses)
        elif choice == "2":
            if not expenses:
                print("No expenses found.")
                continue
            for cat, amt in expenses.items():
                print(f"{cat} : ₹{amt:.2f}")
        elif choice == "3":
            if not expenses:
                print("No expenses found.")
                continue
            total = sum(expenses.values())
            if total == 0:
                print("No expenses found.")
                continue
            highest = max(expenses, key=expenses.get)
            print(f"Total: ₹{total:.2f}")
            print(f"Highest: {highest} - ₹{expenses[highest]:.2f}")
            print("\nCategory Breakdown:")
            for cat, amt in sorted(expenses.items(), key=lambda x: -x[1]):
                percentage = (amt / total) * 100

                if percentage >= 30:
                    print(f"{cat} : {percentage:.2f}% ⚠ High spending!")
                else:
                    print(f"{cat} : {percentage:.2f}%")
            top_two = sorted(expenses.items(), key=lambda x: -x[1])[:2]
            print("\nTop 2 expenses:")
            for cat, amt in top_two:
                print(f"{cat} : ₹{amt:.2f}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")


contacts, expenses = load_data()

while True:
    print("\n ==== MAIN MENU ====")
    print("1. Contact Manager")
    print("2. Expense Manager")
    print("3. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        contact_manager(contacts, expenses)

    elif choice == "2":
        expense_manager(expenses, contacts)

    elif choice == "3":
        save_data(contacts, expenses)
        print("Data saved successfully!")
        break
    else:
        print("Enter a valid choice")
