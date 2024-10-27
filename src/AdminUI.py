from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import os
import sys
from PyQt5.QtCore import pyqtSlot

from src.LoginRoles import LoginRoles

class AdminUI(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
        super(AdminUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.username = username

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'AdminUI.ui')
        loadUi(ui_path, self)

        self.widget.setFixedSize(1000, 500)
        
        self.cancelButton.clicked.connect(self.cancel)
        self.applyButton.clicked.connect(self.userInput)  # Connect apply button to userInput method
        
        
    def userInput(self):
        # Get user account name to modify
        user_account = self.lineEdit.text()
        user_management = LoginRoles()

        # Check which radio button is selected and perform corresponding action
        if self.radioButton.isChecked():  # "Lock" selected
            self.lock_user(user_account, user_management)
        elif self.radioButton_2.isChecked():  # "Unlock" selected
            self.unlock_user(user_account, user_management)
        elif self.radioButton_3.isChecked():  # "Delete" selected
            self.delete_user(user_account, user_management)
        elif self.radioButton_4.isChecked():  # "Make Manager" selected
            self.change_role(user_account, "manager", user_management)
        elif self.radioButton_5.isChecked():  # "Make Pharmacist" selected
            self.change_role(user_account, "pharmacist", user_management)
        elif self.radioButton_6.isChecked():  # "Make Pharmacist Technician" selected
            self.change_role(user_account, "pharmacist technician", user_management)
        elif self.radioButton_7.isChecked():  # "Make Cashier" selected
            self.change_role(user_account, "cashier", user_management)
        elif self.radioButton_8.isChecked():  # "Change Password" selected
            new_password = self.lineEdit_2.text()
            retype_password = self.lineEdit_3.text()
            self.change_password(user_account, new_password, retype_password, user_management)
        else:
            QMessageBox.warning(self, "No Action Selected", "Please select an action to apply.")
            
    # Define the methods to handle each action
    def lock_user(self, user_account, user_management):
        # Implement locking logic
        user_management.lock_account(user_account)
        QMessageBox.information(self, "Lock User", f"{user_account} has been locked.")

    def unlock_user(self, user_account, user_management):
        user_management.reset_locked_counter(user_account)
        QMessageBox.information(self, "Unlock User", f"{user_account} has been unlocked.")

    def delete_user(self, user_account, user_management):
        user_management.remove_account(user_account)
        QMessageBox.information(self, "Delete User", f"{user_account} has been deleted.")

    def change_role(self, user_account, role, user_management):
        user_management.update_account(user_account, new_role=role)
        QMessageBox.information(self, "Change Role", f"{user_account} is now a {role}.")

    def change_password(self, user_account, new_password, retype_password, user_management):
        if new_password != retype_password:
            QMessageBox.warning(self, "Password Mismatch", "The passwords do not match. Please try again.")
        else:
            user_management.update_account(user_account, new_password=new_password)
            QMessageBox.information(self, "Change Password", f"Password for {user_account} has been changed.")
        

    def cancel(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
