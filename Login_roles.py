class Login_Roles(object):
    def __init__(self):
        #REQ-2.5
        self.roles = {
            "manager": {},
            "pharmacist": {},
            "technician": {},
            "cashier": {},
            } # Role type: {dict of username:password}    
        self.failed_login_counter = 0 #REQ-2.6 -> if it reaches 5 failed attempts lock the account
        
        
        
        
        def login(self):
            while self.failed_login_counter < 5:
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role: ")
                if role in self.roles:
                    if username in self.roles[role]:
                        if self.roles[role][username] == password:
                            print("Login successful")
                            break
                        else:
                            print("Invalid password")
                            self.failed_login_counter += 1
                            if self.failed_login_counter == 5:
                                print("Account locked")
                                break
                    else:
                        print("Invalid username")
                else:
                    print("Invalid role")
            return