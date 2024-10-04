import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file

from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QLineEdit, QStackedWidget
from PyQt5.uic import loadUi
from src.Dashboard import Dashboard  # Import the Dashboard UI


class MainUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(MainUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'LogInGUI.ui')
        loadUi(ui_path, self)

        # Connect buttons to their actions
        self.logInButton.clicked.connect(self.logIn)
        self.password.setEchoMode(QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.createAccount)

    def logIn(self):
        userName = self.userName.text()
        password = self.password.text()
        
        # Add your login validation logic here. For now, assume login is successful.
        if userName == "admin" and password == "password":  # Example check
            dashboard = Dashboard(self.widget)  # Create the dashboard instance
            self.widget.addWidget(dashboard)  # Add dashboard to the stacked widget
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)  # Switch to Dashboard
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Login Failed")
            msg.setText("Incorrect username or password!")
            msg.exec_()


    def createAccount(self):
        # Create the account creation UI and add it to the stacked widget
        createacc = CreateAccountUI(self.widget)  # Pass the widget to CreateAccountUI
        self.widget.addWidget(createacc)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)  # Switch to CreateAccountUI


class CreateAccountUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(CreateAccountUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'createAccount.ui')
        loadUi(ui_path, self)

        # Connect the "Create Account" button to its action
        self.createAccountButton.clicked.connect(self.createAccount)

    def createAccount(self):
        userName = self.createUserName.text()
        email = self.email.text()
        password = self.createPassword.text()

        # Show password input dialog with masked input
        manager_password, ok = QInputDialog.getText(self, 'Manager Login', 'Enter manager password:', QLineEdit.Password)

        # Check if the user pressed OK and handle the password check
        if ok:
            if manager_password == '123':  # Replace with the actual manager password
                msg = QMessageBox()
                msg.setWindowTitle("Access Granted")
                msg.setText("Welcome, Manager!")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Access Denied")
                msg.setText("Incorrect password!")
                msg.exec_()

