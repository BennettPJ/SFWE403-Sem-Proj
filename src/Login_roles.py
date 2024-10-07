class LoginRoles:
    def __init__(self):
        """Initialize roles and failed login counter."""
        self.roles = {
            "manager": {},
            "pharmacist": {},
            "technician": {},
            "cashier": {},
            "patient": {},
        }  # Role type: {dict of username:password}
        self.failed_login_counter = 0  # Lock the account after 5 failed attempts

    def login(self):
        """Handles user login with role-based access."""
        while self.failed_login_counter < 5:
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: ")

            if role in self.roles:
                if username in self.roles[role]:
                    if self.roles[role][username] == password:
                        print("Login successful")
                        self.failed_login_counter = 0  
                        return True
                    else:
                        print("Invalid password")
                        self.failed_login_counter += 1
                        if self.failed_login_counter == 5:
                            print("Account locked")
                            return False
                else:
                    print("Invalid username")
            else:
                print("Invalid role")
        return False

    def create_account(self, role: str, username: str, password: str) -> bool:
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
