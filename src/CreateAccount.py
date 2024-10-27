# CreateAccount.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from PyQt5.uic import loadUi


class CreateAccountUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(CreateAccountUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'createAccount.ui')
        loadUi(ui_path, self)
        
        # Set fixed size for the create account screen
        self.setFixedSize(1000, 600)  # Use setFixedSize instead of setMinimumSize

        # Connect the buttons to their actions
        self.signUpButton.clicked.connect(self.createAccount)
        self.logIn2.clicked.connect(self.returnToLogin)  # Log In button to go back to MainUI

    def createAccount(self):
        username = self.createUserName.text()  
        email = self.email.text()
        password = self.createPassword.text() 
        repassword = self.reEnterPass.text() 
        role = self.rolesBox.currentText() 
        
        from src.LoginRoles import LoginRoles
        
        roles = LoginRoles() 
        
        if password != repassword:
            msg = QMessageBox()
            msg.setWindowTitle("Password Mismatch")
            msg.setText("Passwords do not match. Please re-enter your password.")
            msg.exec_()
        else:
            roles.create_account(role, username, password, email)
            msg = QMessageBox()
            msg.setWindowTitle("Account Created")
            msg.setText("Your account has been created successfully!")
            msg.exec_()
            self.returnToLogin()

    def returnToLogin(self):
        """
        Return to the login screen when 'Log In' is clicked in the CreateAccount screen.
        Avoid duplicate MainUI instances by checking if it already exists in the widget stack.
        """
        from src.LogInGUI import MainUI  # Import MainUI inside the function to avoid circular import

        # Check if MainUI (login screen) is already in the stack to avoid duplicates
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                self.widget.setCurrentIndex(i)
                self.widget.setFixedSize(800, 525)  # Resize to match login screen
                return

        # If not found, create a new MainUI instance
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
        self.widget.setFixedSize(800, 525)  # Resize to match login screen
