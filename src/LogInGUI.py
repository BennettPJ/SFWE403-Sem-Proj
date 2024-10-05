#LogInGUI.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from src.Dashboard import Dashboard  # Import the Dashboard UI
from src.CreateAccount import CreateAccountUI  # Import CreateAccountUI


class MainUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(MainUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'LogInGUI.ui')
        loadUi(ui_path, self)

        print("MainUI created and buttons connected.")

        # Connect buttons to their actions
        self.logInButton.clicked.connect(self.logIn)
        self.password.setEchoMode(QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.createAccount)

    def logIn(self):
        """
        Handle the login logic.
        """
        userName = self.userName.text()
        password = self.password.text()
        
        if userName == "admin" and password == "password":
            # Check if the dashboard is already in the stacked widget
            for i in range(self.widget.count()):
                if isinstance(self.widget.widget(i), Dashboard):
                    self.widget.setCurrentIndex(i)  # Switch to existing Dashboard
                    return
            
            # If not found, create the dashboard and add it to the stacked widget
            dashboard = Dashboard(self.widget)
            self.widget.addWidget(dashboard)
            self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        else:
            # Display a message if login fails
            msg = QMessageBox()
            msg.setWindowTitle("Login Failed")
            msg.setText("Incorrect username or password!")
            msg.exec_()

    def createAccount(self):
        """
        Switch to the create account screen. Check if it already exists.
        """
        print("Create Account button clicked")  # Debugging

        # Check if CreateAccountUI is already in the stacked widget
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), CreateAccountUI):
                print("CreateAccountUI already exists, switching to it.")
                self.widget.setCurrentIndex(i)  # Switch to existing CreateAccountUI
                return

        # If not found, create the account creation UI and add it to the stacked widget
        createacc = CreateAccountUI(self.widget)
        self.widget.addWidget(createacc)  # Add CreateAccountUI to the stacked widget
        print("Switching to Create Account screen")  # Debugging
        self.widget.setCurrentIndex(self.widget.indexOf(createacc))

