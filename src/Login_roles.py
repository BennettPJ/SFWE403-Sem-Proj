class Login_Roles(object):
    def __init__(self):
        # REQ-2.5: User authentication for all roles
        self.roles = {
            "manager": {},
            "pharmacist": {},
            "technician": {},
            "cashier": {},
        }  # Role type: {dict of username:password}
        
        self.failed_login_counter = {}  # Track failed attempts per user for REQ-2.6
        self.locked_accounts = set()  # Track locked accounts for REQ-2.6 & REQ-2.7
    
    # REQ-2.2, 2.3, 2.5, 2.6: Login functionality with password creation on first login
    def login(self):
        username = input("Enter username: ")
        role = input("Enter role: ")
        
        if username in self.locked_accounts: #checks of the account has been locked 
            print("Account is locked. Please contact the manager.")
            return
        
        if role in self.roles and username in self.roles[role]:
            if username not in self.failed_login_counter:
                self.failed_login_counter[username] = 0
                
            # Handle first-time login (REQ-2.3)
            if self.roles[role][username]["first_login"]:
                new_password = input("First login! Please create a new password: ")
                self.roles[role][username]["password"] = new_password
                self.roles[role][username]["first_login"] = False
                print("Password created successfully!")
            else:
                password = input("Enter password: ")
                if self.roles[role][username]["password"] == password:
                    print("Login successful")
                    self.failed_login_counter[username] = 0  # Reset counter on success
                else:
                    print("Invalid password")
                    self.failed_login_counter[username] += 1
                    if self.failed_login_counter[username] >= 5:
                        print("Account locked after 5 failed attempts")
                        self.locked_accounts.add(username)  # Lock the account (REQ-2.6)
        else:
            print("Invalid role or username")
    
    # REQ-2.4: Authorized user can change password
    def change_password(self, role, username):
        if role in self.roles and username in self.roles[role]:
            old_password = input("Enter current password: ")
            if self.roles[role][username]["password"] == old_password:
                new_password = input("Enter new password: ")
                self.roles[role][username]["password"] = new_password
                print("Password changed successfully!")
            else:
                print("Incorrect current password")
        else:
            print("Invalid role or username")