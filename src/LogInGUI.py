import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from src.Dashboard import Dashboard  # Import the Dashboard UI
from src.CreateAccount import CreateAccountUI  # Import CreateAccountUI
from LoginRoles import LoginRoles

class MainUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(MainUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.login_roles = LoginRoles()  # Initialize login roles
        # Load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'LogInGUI.ui')
        loadUi(ui_path, self)

        # Set fixed dimensions for the login screen
        self.setFixedSize(800, 525) 
        
        # Connect buttons to actions
        self.logInButton.clicked.connect(self.logIn)
        self.password.setEchoMode(QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.createAccount)

    def logIn(self):
        try:
            userName = self.userName.text()
            password = self.password.text()
            
            success, message = self.login_roles.login(userName, password)

            if success:
                # Check if Dashboard already exists in the stack to avoid duplicate instances
                for i in range(self.widget.count()):
                    if isinstance(self.widget.widget(i), Dashboard):
                        self.widget.setCurrentIndex(i)
                        self.widget.setFixedSize(1050, 600)  # Resize for dashboard
                        return
                
                # Create new Dashboard instance if it doesn't exist
                dashboard = Dashboard(self.widget)
                self.widget.addWidget(dashboard)
                self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
                self.widget.setFixedSize(1050, 600)  # Resize for dashboard
            else:
                # Show message if login fails
                msg = QMessageBox()
                msg.setWindowTitle("Login Failed")
                msg.setText(message)
                msg.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            print(f"Error during login: {e}")

    def createAccount(self):
        # Check if CreateAccountUI is already in the stack to avoid duplicates
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), CreateAccountUI):
                self.widget.setCurrentIndex(i)
                self.widget.setFixedSize(1000, 600)  # Resize for Create Account screen
                return

        # Create new instance if not found
        createacc = CreateAccountUI(self.widget)
        self.widget.addWidget(createacc)
        self.widget.setCurrentIndex(self.widget.indexOf(createacc))
        self.widget.setFixedSize(1000, 600)  # Resize for Create Account screen
