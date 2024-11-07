import csv
import os
import logging

class LoginRoles:
    def __init__(self, roles_file='../DBFiles/db_user_account.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.roles_file = os.path.join(base_path, roles_file)
        self.default_admin = {
            "username": "adminLogin",
            "email": "admin@admin.com",
            "password": "SuperSecretPassword",
            "role": "manager",
            "locked_counter": "0",
            "locked_status": "unlocked"
        }

        # Ensure the CSV file exists
        if not os.path.exists(self.roles_file):
            with open(self.roles_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])
                writer.writerow([
                    self.default_admin['username'],
                    self.default_admin['email'],
                    self.default_admin['password'],
                    self.default_admin['role'],
                    self.default_admin['locked_counter'],
                    self.default_admin['locked_status']
                ])
        
        # Setup logging
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'transaction.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    def log_transaction(self, event):
        logging.info(event)

    # Example of an updated login function with logging
    def login(self, username: str, password: str):
        user_data = self.get_user_data(username)
        
        if user_data:
            if user_data['Locked_status'] == 'locked':
                self.log_transaction(f"Attempted login to locked account: {username}")
                return False, "Account locked due to too many failed attempts"
            if user_data['Password'] == password:
                self.reset_locked_counter(username)
                self.log_transaction(f"Login successful for user: {username}")
                return True, f"Login successful as {user_data['Role']}."
            else:
                self.increment_locked_counter(username)
                self.log_transaction(f"Failed login for user: {username}")
                return False, "Invalid password"
        else:
            self.log_transaction(f"Failed login with non-existent username: {username}")
            return False, "Invalid username"

    def find_user_role(self, username: str):
        """Find the role of a non-admin user based on the username."""
        user_data = self.get_user_data(username)
        return user_data['Role'] if user_data else None

    def create_account(self, role: str, username: str, password: str, email: str):
        """Creates a new user account."""
        if self.account_exists(username):
            print("Username already exists.")
            return False

        with open(self.roles_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password, role, '0', 'unlocked'])
        print(f"User '{username}' added to role '{role}'.")
        return True

    def remove_account(self, username: str):
        """Removes a user account."""
        rows = []
        found = False
        try:
            with open(self.roles_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] != username:
                        rows.append([row['Username'], row['Email'], row['Password'], row['Role'], row['Locked_counter'], row['Locked_status']])
                    else:
                        found = True

            if found:
                with open(self.roles_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])
                    writer.writerows(rows)
                print(f"User '{username}' removed.")
                return True
            else:
                print("Username not found.")
                return False
        except FileNotFoundError:
            print("Roles file not found.")
            return False

    def account_exists(self, username: str):
        """Checks if an account already exists for the given username."""
        return self.get_user_data(username) is not None

    def get_user_data(self, username: str):
        """Helper method to retrieve user data from the CSV based on the username."""
        try:
            with open(self.roles_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username:
                        return row
        except FileNotFoundError:
            print("Roles file not found.")
        return None

    def increment_locked_counter(self, username: str):
        """Increments the locked counter and locks the account if it reaches 5 failed attempts."""
        rows = []
        user_found = False
        try:
            with open(self.roles_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username:
                        user_found = True
                        locked_counter = int(row['Locked_counter']) + 1
                        locked_status = 'locked' if locked_counter >= 5 else 'unlocked'
                        row['Locked_counter'] = str(locked_counter)
                        row['Locked_status'] = locked_status
                    rows.append([row['Username'], row['Email'], row['Password'], row['Role'], row['Locked_counter'], row['Locked_status']])

            if user_found:
                with open(self.roles_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])
                    writer.writerows(rows)

        except FileNotFoundError:
            print("Roles file not found.")

    def reset_locked_counter(self, username: str):
        """Resets the locked counter and unlocks the account."""
        rows = []
        user_found = False
        try:
            with open(self.roles_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username:
                        user_found = True
                        row['Locked_counter'] = '0'
                        row['Locked_status'] = 'unlocked'
                    rows.append([row['Username'], row['Email'], row['Password'], row['Role'], row['Locked_counter'], row['Locked_status']])

            if user_found:
                with open(self.roles_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])
                    writer.writerows(rows)

        except FileNotFoundError:
            print("Roles file not found.")
            
    def lock_account(self, username: str):
        """Sets the locked counter to 5 and locks the account."""
        rows = []
        user_found = False
        try:
            with open(self.roles_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username:
                        user_found = True
                        row['Locked_counter'] = '5'
                        row['Locked_status'] = 'locked'
                    rows.append([row['Username'], row['Email'], row['Password'], row['Role'], row['Locked_counter'], row['Locked_status']])

            if user_found:
                with open(self.roles_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])
                    writer.writerows(rows)
            else:
                print(f"User '{username}' not found.")

        except FileNotFoundError:
            print("Roles file not found.")
            
    def update_account(self, username: str, new_email=None, new_password=None, new_role=None):
        """Updates an existing user account's email, password, or role."""
        rows = []
        user_found = False
        try:
            with open(self.roles_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username:
                        user_found = True
                        # Update fields if new values are provided
                        if new_email:
                            row['Email'] = new_email
                        if new_password:
                            row['Password'] = new_password
                        if new_role:
                            row['Role'] = new_role
                    rows.append([row['Username'], row['Email'], row['Password'], row['Role'], row['Locked_counter'], row['Locked_status']])

            if user_found:
                with open(self.roles_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])
                    writer.writerows(rows)
                print(f"User '{username}' updated.")
                return True
            else:
                print("Username not found.")
                return False
        except FileNotFoundError:
            print("Roles file not found.")
            return False