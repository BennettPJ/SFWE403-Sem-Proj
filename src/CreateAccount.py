# Import necessary libraries for PyQt5 and system operations
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from src.LoginRoles import LoginRoles

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

class CreateAccountUI(QMainWindow):
    # Constructor that accepts the widget as a parameter
    def __init__(self, widget):  
        super(CreateAccountUI, self).__init__()
        self.widget = widget 
        
        # Create an instance of the LoginRoles class
        self.roles = LoginRoles() 

        # Load the UI file relative to the project's root directory
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'createAccount.ui')
        loadUi(ui_path, self)
        
        # Set fixed size for the create account screen
        self.setFixedSize(1000, 600) 

        # Connect the Sign Up and Log In buttons to their respective functions when press
        self.signUpButton.clicked.connect(self.createAccount)
        self.logIn2.clicked.connect(self.returnToLogin)  

    # Function to handle account creation logic
    def createAccount(self):
        username = self.createUserName.text() # Get the entered username
        email = self.email.text() # Get the entered email
        password = self.createPassword.text()  # Get the entered password
        repassword = self.reEnterPass.text()  # Get the re-entered password
        role = self.rolesBox.currentText() # Get the selected role from the dropdown
        
        # Check if the passwords match
        if password != repassword:
            # Display a warning popup if passwords do not match
            msg = QMessageBox()
            msg.setWindowTitle("Password Mismatch")
            msg.setText("Passwords do not match. Please re-enter your password.")
            msg.exec_()
        else:
            # Call the create_account function from LoginRoles to create the new account
            self.roles.create_account(role, username, password, email)
            # Display a popup for successful creation of account
            msg = QMessageBox()
            msg.setWindowTitle("Account Created")
            msg.setText("Your account has been created successfully!")
            msg.exec_()
            self.returnToLogin() # Return to the login screen after successful account creation

    # Function to navigate back to the login screen
    def returnToLogin(self):
        from src.LogInGUI import MainUI  # Import MainUI inside the function to avoid circular import
        # Check if login screen is in the stack to avoid duplicates
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                self.widget.setCurrentIndex(i)
                self.widget.setFixedSize(800, 525)  
                return

        # If the MainUI instance is not found, create a new one
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
        self.widget.setFixedSize(800, 525)  # Set the window title and dimensions