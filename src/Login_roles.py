class LoginRoles:
    def __init__(self):
        """Initialize roles, hardcoded admin, and failed login counter."""
        # Hardcoded admin as manager
        self.default_admin = {
            "username": "admin",
            "password": "password",
            "role": "manager"
        }

        self.roles = {
            "manager": {},
            "pharmacist": {},
            "technician": {},
            "cashier": {},
            "patient": {},
        }  # Role type: {dict of username:password}
        self.failed_login_counter = 0  # Lock the account after 5 failed attempts

    def login(self, username: str, password: str):
        """Handles user login with role-based access."""
        if self.failed_login_counter >= 5:
            return False, "Account locked due to too many failed attempts"

        # Check if the user is the hardcoded admin
        if username == self.default_admin['username'] and password == self.default_admin['password']:
            self.failed_login_counter = 0  # Reset counter on successful admin login
            return True, "Login successful as manager (admin)."

        # Check dynamic roles for other users
        role = self.find_user_role(username)
        if role:
            if username in self.roles[role]:
                if self.roles[role][username] == password:
                    self.failed_login_counter = 0  # Reset counter on successful login
                    return True, f"Login successful as {role}."
                else:
                    self.failed_login_counter += 1
                    return False, "Invalid password"
            else:
                return False, "Invalid username"
        else:
            return False, "Invalid role"

    def find_user_role(self, username: str):
        """Find the role of a non-admin user based on the username."""
        for role, users in self.roles.items():
            if username in users:
                return role
        return None  # Return None if no role matches

    def create_account(self, role: str, username: str, password: str):
        """Creates a new user account."""
        if role in self.roles:
            if username in self.roles[role]:
                print("Username already exists.")
                return False 
            self.roles[role][username] = password
            print(f"User '{username}' added to role '{role}'.")
            return True
        print("Invalid role specified.")
        return False
