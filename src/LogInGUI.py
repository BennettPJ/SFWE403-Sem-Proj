import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QLineEdit
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
            userName = str(userName)
            password = str(password)
            
            # Call the back-end login method
            roles = LoginRoles() 
            success, message = roles.login(userName, password)
            

            if success:
                # Check if the dashboard is already in the stacked widget
                # Remove any previous instances of Dashboard
                for i in range(self.widget.count()):
                    if isinstance(self.widget.widget(i), Dashboard):
                        self.widget.removeWidget(self.widget.widget(i))
                        

                
                # If not found, create the dashboard and add it to the stacked widget
                dashboard = Dashboard(self.widget, userName)  # Assuming you have a Dashboard class

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

            error_message = f"Error during login: {e}"
            QMessageBox.critical(self, "Error", error_message)  # Show the error if any
            print(error_message)
            

    def createAccount(self):
        """Switch to the create account screen. Check if it already exists. Requires pharmacy manager login before allowing access."""
        manager_username, ok = QInputDialog.getText(self, "Manager Approval", "Enter Manager Username:")
        if not ok or not manager_username:
            QMessageBox.warning(self, "Account Creation Cancelled", "Manager approval is required to create an account.")
            return

        # Prompt for manager password
        manager_password, ok = QInputDialog.getText(self, "Manager Approval", "Enter Manager Password:", QLineEdit.Password)
        if not ok or not manager_password:
            QMessageBox.warning(self, "Account Creation Cancelled", "Manager approval is required to create an account.")
            return

        # Verify manager credentials
        roles = LoginRoles()
        success, message = roles.login(manager_username, manager_password)
        if not success or roles.find_user_role(manager_username) != 'manager':
            msg = QMessageBox()
            msg.setWindowTitle("Authorization Failed")
            msg.setText("Manager approval failed. Please try again.")
            msg.exec_()
            return

        # If manager approval is successful, switch to the create account screen
        print("Manager authenticated. Loading Create Account screen.")

        # Check if CreateAccountUI is already in the stacked widget

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
