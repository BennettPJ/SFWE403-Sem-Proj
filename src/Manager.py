class Manager:
    def __init__(self, login_system):
        self.login_system = login_system
    
    # REQ-2.1: Manager creates user accounts
    def create_user_account(self):
        role = input("Enter the role (manager, pharmacist, technician, cashier): ")
        if role not in self.login_system.roles: #sets and checks if the role is a valid one 
            print(f"Invalid role: {role}")
            return

        username = input("Enter the new username: ") #sets the username for the new account
        if username in self.login_system.roles[role]:
            print(f"User {username} already exists!")#checks if the username already exists 
            return
        
        password = input("Enter the initial password for the new user: ") #sets the first password for the account 
        self.login_system.roles[role][username] = {"password": password, "first_login": True}
        print(f"User account created for {username} in role {role}")
    
    # REQ-2.7: Only the manager can unlock accounts
    def unlock_account(self):
        username_to_unlock = input("Enter the username to unlock: ")
        if username_to_unlock in self.login_system.locked_accounts: #finds the locked account 
            self.login_system.locked_accounts.remove(username_to_unlock)
            self.login_system.failed_login_counter[username_to_unlock] = 0  # Reset failed attempts
            print(f"Account {username_to_unlock} unlocked by the manager")
        else:
            print("User account is not locked or does not exist")