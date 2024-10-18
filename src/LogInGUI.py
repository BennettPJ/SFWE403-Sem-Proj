import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from src.Dashboard import Dashboard  # Import the Dashboard UI
from src.CreateAccount import CreateAccountUI  # Import CreateAccountUI
from Login_roles import LoginRoles

class MainUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(MainUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.login_roles = LoginRoles()  # Ensure login_roles is initialized here
        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'LogInGUI.ui')
        loadUi(ui_path, self)

        print("MainUI created and buttons connected.")

        # Connect buttons to their actions
        self.logInButton.clicked.connect(self.logIn)
        self.password.setEchoMode(QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.createAccount)

    def logIn(self):
        try:
            """
            Handle the login logic.
            """
            userName = self.userName.text()
            password = self.password.text()
            
        # Call the back-end login method
            success, message = self.login_roles.login(userName, password)

            if success:
                
                # Check if the dashboard is already in the stacked widget
                for i in range(self.widget.count()):
                    if isinstance(self.widget.widget(i), Dashboard):  # Check if the dashboard already exists
                        self.widget.setCurrentIndex(i)  # Switch to existing Dashboard
                        self.resizeToCurrentWidget()  # Ensure proper resizing
                        return
                
                # If not found, create the dashboard and add it to the stacked widget
                dashboard = Dashboard(self.widget)  # Assuming you have a Dashboard class
                self.widget.addWidget(dashboard)
                self.widget.setCurrentIndex(self.widget.indexOf(dashboard))  # Switch to the new Dashboard
                self.resizeToCurrentWidget()  # Ensure proper resizing
            else:
                # Show an error message if login fails
                msg = QMessageBox()
                msg.setWindowTitle("Login Failed")
                msg.setText(message)
                msg.exec_()
        except Exception as e:
                QMessageBox.critical(self, "Error", str(e))  # Show the error if any
                print(f"Error during login: {e}")

    def createAccount(self):
        """
        Switch to the create account screen. Check if it already exists.
        """
        print("Create Account button clicked")  # Debugging

        # Check if CreateAccountUI is already in the stacked widget
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), CreateAccountUI):
                self.widget.setCurrentIndex(i)  # Switch to existing CreateAccountUI
                self.resizeToCurrentWidget()  # Ensure proper resizing
                return

        # If not found, create the account creation UI and add it to the stacked widget
        createacc = CreateAccountUI(self.widget)
        self.widget.addWidget(createacc)  # Add CreateAccountUI to the stacked widget
        self.widget.setCurrentIndex(self.widget.indexOf(createacc))
        self.resizeToCurrentWidget()  # Ensure proper resizing

    def resizeToCurrentWidget(self):
        """
        Resize the QStackedWidget to fit the current widget (MainUI, Dashboard, CreateAccountUI).
        """
        current_widget = self.widget.currentWidget()  # Get the current widget
        self.widget.resize(current_widget.width(), current_widget.height())  # Resize to match the current widget

