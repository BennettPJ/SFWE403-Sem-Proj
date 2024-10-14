#CreateAccount.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class CreateAccountUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(CreateAccountUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'createAccount.ui')
        loadUi(ui_path, self)

        # Connect the buttons to their actions
        self.signUpButton.clicked.connect(self.createAccount)
        self.logIn2.clicked.connect(self.returnToLogin)  # Log In button to go back to MainUI

    def createAccount(self):
        # Handle the account creation logic here
        pass

    def returnToLogin(self):
        """
        Return to the login screen when 'Log In' is clicked in the CreateAccount screen.
        Always create a new instance of MainUI to ensure fresh button connections.
        """

        from src.LogInGUI import MainUI  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))

