import sys
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QComboBox
from PyQt5.uic import loadUi
from src.Login_roles import LoginRoles
from src.Dashboard import Dashboard

class CreateAccountUI(QMainWindow):
    def __init__(self, widget):
        super(CreateAccountUI, self).__init__()
        self.widget = widget

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'createAccount.ui')
        loadUi(ui_path, self)

        # Find UI components by their object names
        self.usernameInput = self.findChild(QLineEdit, 'usernameInput')
        self.passwordInput = self.findChild(QLineEdit, 'passwordInput')
        self.roleInput = self.findChild(QComboBox, 'roleInput')

        # Instantiate the LoginRoles class
        self.login_roles = LoginRoles()

        # Connect buttons to their actions
        self.signUpButton.clicked.connect(self.create_account)
        self.logIn2.clicked.connect(self.returnToLogin)

    def create_account(self):
        """Handle account creation logic."""
        username = self.createUserName.text().strip()
        email = self.email.text().strip()
        password = self.createPassword.text().strip()
        role = self.rolesBox.currentText()  # Get selected role

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return

        if self.login_roles.create_account(role, username, password):
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.returnToLogin()  # Optionally switch back to login UI
        else:
            QMessageBox.warning(self, "Account Creation Failed", "Username already exists or invalid role.")

    def returnToLogin(self):
        from src.LogInGUI import MainUI
        """Return to the login screen."""
        print("Returning to login screen.")
        self.widget.setCurrentIndex(self.widget.indexOf(MainUI(self.widget)))
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'LogInGUI.ui')
        loadUi(ui_path, self)
        
