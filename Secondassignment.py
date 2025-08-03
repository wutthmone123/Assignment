
import os

class MiniBank:

    user_file = "user_datalist.txt"

    def firstOption(self):
        try:
            option = int(input("Press 1 to Login\nPress 2 to Register: "))
            if option == 1:
                self.login()
            elif option == 2:
                self.register()
            else:
                print("Invalid option.")
        except Exception as error:
            print(error)


    def write_users(self, users):
        with open(self.user_file, "w") as f:
            for user in users:
                line = f"{user['id']},{user['username']},{user['password']},{user['amount']}\n"
                f.write(line)

    def register(self):
        print("-------- This is from Register page --------")
        users = self.read_users()
        r_username = input("Please enter username to register: ")

        if self.find_user(r_username, users):
            print("Username already exists.")
            return

        r_amount = int(input("Please enter your amount: "))
        passcode1 = int(input("Please enter password to register: "))
        passcode2 = int(input("Please enter confirm password to register: "))

        if passcode1 != passcode2:
            print("Passwords do not match.")
            return

        user_id = len(users) + 1
        users.append({
            "id": user_id,
            "username": r_username,
            "password": passcode2,
            "amount": r_amount
        })
        self.write_users(users)
        print("Registration successful.")


    def read_users(self):
        users = []
        if not os.path.exists(self.user_file):
            return users

        with open(self.user_file, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    user_id = int(parts[0])
                    username = parts[1]
                    password = int(parts[2])
                    amount = int(parts[3])
                    users.append({
                        "id": user_id,
                        "username": username,
                        "password": password,
                        "amount": amount
                    })
        return users

    def login(self):
        print("-------- This is from Login page --------")
        users = self.read_users()
        l_username = input("Please enter your username: ")
        l_passcode = int(input("Please enter your passcode: "))

        user = self.find_user(l_username, users)
        if user and user["password"] == l_passcode:
            print("Login successful.")
            self.menu(user["id"])
        else:
            print("Invalid username or password.")



    def find_user(self, username, users):
        for user in users:
            if user["username"] == username:
                return user
        return None


    def menu(self, login_id):
        users = self.read_users()
        user = next((u for u in users if u["id"] == login_id), None)
        if not user:
            print("User not found.")
            return

        menu_input = int(input("Press 1 to Transfer\nPress 2 to Withdraw Info\nPress 3 to Update Info:\n"))

        if menu_input == 1:
            if len(users) < 2:
                print("Transfer not possible. Only one user exists.")
                return

            transfer_username = input("Enter username to transfer to: ")
            accept_user = self.find_user(transfer_username, users)

            if not accept_user:
                print("Recipient not found.")
                return
            if accept_user["id"] == login_id:
                print("Cannot transfer to yourself.")
                return

            amount = int(input("Enter amount to transfer: "))
            if user["amount"] >= amount:
                user["amount"] -= amount
                accept_user["amount"] += amount
                print("Transfer successful.")
                print(f"You transferred {amount} to {accept_user['username']}")
                self.write_users(users)
            else:
                print("Insufficient balance.")

        elif menu_input == 2:
            print("\n--- Withdraw Info ---")
            print(f"Username: {user['username']}")
            print(f"Balance: {user['amount']}")

        elif menu_input == 3:
            update_input = int(input("Press 1 to Change Name\nPress 2 to Change Amount\nPress 3 to Change Password:\n"))
            if update_input == 1:
                new_name = input("Enter new username: ")
                if self.find_user(new_name, users):
                    print("Username already taken.")
                    return
                user["username"] = new_name
                print("Username updated.")
            elif update_input == 2:
                new_amount = int(input("Enter new amount: "))
                user["amount"] = new_amount
                print("Amount updated.")
            elif update_input == 3:
                new_pass = int(input("Enter new password: "))
                user["password"] = new_pass
                print("Password updated.")
            else:
                print("Invalid option.")
            self.write_users(users)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    bank = MiniBank()
    while True:
        bank.firstOption()
