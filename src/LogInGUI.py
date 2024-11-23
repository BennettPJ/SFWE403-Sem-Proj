import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QLineEdit
from PyQt5.uic import loadUi
from Dashboard import Dashboard  # Import the Dashboard UI
from CreateAccount import CreateAccountUI  # Import CreateAccountUI
from StoreHoursUI import StoreHoursUI  # Import StoreHoursUI
from LoginRoles import LoginRoles

class MainUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(MainUI, self).__init__()
        self.widget = widget  
        
        # Initialize login roles
        self.login_roles = LoginRoles()  
        
        # Load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'LogInGUI.ui')
        loadUi(ui_path, self)

        # Set fixed dimensions for the login screen
        self.setFixedSize(800, 525) 
        
        # Connect buttons to actions
        self.logInButton.clicked.connect(self.logIn)
        self.password.setEchoMode(QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.createAccount)
        self.storeHoursButton.clicked.connect(self.store_hours)


    def logIn(self):
        # Allow the user to log in to the system via username and password
        try:
            userName = self.userName.text()
            password = self.password.text()
            userName = str(userName)
            password = str(password)
            
            # Call the back-end login method to see if user is valid
            success, message = self.login_roles.login(userName, password)
            
            if success:
                # Check if the dashboard is already in the stacked widget
                # Remove any previous instances of Dashboard so its updated for the new users role
                for i in range(self.widget.count()):
                    if isinstance(self.widget.widget(i), Dashboard):
                        self.widget.removeWidget(self.widget.widget(i))
                        
                # If not found, create the dashboard and add it to the stacked widget
                dashboard = Dashboard(self.widget, userName)  

                self.widget.addWidget(dashboard)
                self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
                self.widget.setFixedSize(1050, 600)  
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
        # Prompt for manager username and password to create a new account and switch to the create account screen
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
        success, message = self.login_roles.login(manager_username, manager_password)
        if not success or self.login_roles.find_user_role(manager_username) != 'manager':
            msg = QMessageBox()
            msg.setWindowTitle("Authorization Failed")
            msg.setText("Manager approval failed. Please try again.")
            msg.exec_()
            return

        # Check if CreateAccountUI is already in the stacked widget
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), CreateAccountUI):
                self.widget.setCurrentIndex(i)
                self.widget.setFixedSize(1000, 600)  
                return

        # Create new instance if not found
        createacc = CreateAccountUI(self.widget)
        self.widget.addWidget(createacc)
        self.widget.setCurrentIndex(self.widget.indexOf(createacc))
        self.widget.setFixedSize(1000, 600)  


    def store_hours(self):
        # Store hours of operation screen
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), StoreHoursUI):
                self.widget.setCurrentIndex(i)
                self.widget.setFixedSize(1000, 600)  
                return

        # Create new instance if not found
        storehours = StoreHoursUI(self.widget)
        self.widget.addWidget(storehours)
        self.widget.setCurrentIndex(self.widget.indexOf(storehours))
        self.widget.setFixedSize(1000, 600) 