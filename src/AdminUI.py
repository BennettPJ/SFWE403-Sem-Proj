# Import necessary libraries for PyQt5 and system operations
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from src.LoginRoles import LoginRoles

class AdminUI(QMainWindow):
    #Constructor class that accepts the widget and username as parameters
    def __init__(self, widget, username):
        super(AdminUI, self).__init__()
        self.widget = widget
        self.username = username
        
        #create an instance of the LoginRoles class
        self.user_management = LoginRoles()

        # Load the UI file relative to the project's root directory
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'AdminUI.ui')
        loadUi(ui_path, self)

        # Set the window title and dimensions
        self.widget.setFixedSize(1000, 500)
        
        # Set the Cancel button and the apply button to call their respective functions when pressed
        self.cancelButton.clicked.connect(self.cancel)
        self.applyButton.clicked.connect(self.userInput)  
        
    # The UserInput function is called when the apply button is pressed
    #This function expects no parameters
    def userInput(self):
        # Get the user entered account name
        user_account = self.lineEdit.text()

        # Check which radio button is selected and perform corresponding action
        if self.radioButton.isChecked():  # "Lock" selected
            self.lock_user(user_account, self.user_management)
            
        elif self.radioButton_2.isChecked():  # "Unlock" selected
            self.unlock_user(user_account, self.user_management)
            
        elif self.radioButton_3.isChecked():  # "Delete" selected
            self.delete_user(user_account, self.user_management)
            
        elif self.radioButton_4.isChecked():  # "Make Manager" selected
            self.change_role(user_account, "manager", self.user_management)
            
        elif self.radioButton_5.isChecked():  # "Make Pharmacist" selected
            self.change_role(user_account, "pharmacist", self.user_management)
            
        elif self.radioButton_6.isChecked():  # "Make Pharmacist Technician" selected
            self.change_role(user_account, "pharmacist technician", self.user_management)
            
        elif self.radioButton_7.isChecked():  # "Make Cashier" selected
            self.change_role(user_account, "cashier", self.user_management)
            
        elif self.radioButton_8.isChecked():  # "Change Password" selected
            new_password = self.lineEdit_2.text()
            retype_password = self.lineEdit_3.text()
            self.change_password(user_account, new_password, retype_password, self.user_management)
            
        else:
            #Display a warning to the user in the form of a popup that no action was selected and they need to select one.
            QMessageBox.warning(self, "No Action Selected", "Please select an action to apply.")
            

    ########### The following functions are called when the corresponding radio button is selected ############
    def lock_user(self, user_account, user_management):
        user_management.lock_account(user_account)
        #Display a popup to the user that the account has been locked
        QMessageBox.information(self, "Lock User", f"{user_account} has been locked.")


    def unlock_user(self, user_account, user_management):
        user_management.reset_locked_counter(user_account)
        # Display a popup to the user that the account has been unlocked
        QMessageBox.information(self, "Unlock User", f"{user_account} has been unlocked.")


    def delete_user(self, user_account, user_management):
        user_management.remove_account(user_account)
        # Display a popup to the user that the account has been deleted
        QMessageBox.information(self, "Delete User", f"{user_account} has been deleted.")


    def change_role(self, user_account, role, user_management):
        user_management.update_account(user_account, new_role=role)
        # Display a popup to the user that the role has been changed
        QMessageBox.information(self, "Change Role", f"{user_account} is now a {role}.")


    def change_password(self, user_account, new_password, retype_password, user_management):
        if new_password != retype_password:
            # Display a warning to the user in the form of a popup that the passwords do not match
            QMessageBox.warning(self, "Password Mismatch", "The passwords do not match. Please try again.")
        else:
            user_management.update_account(user_account, new_password=new_password)
            # Display a popup to the user that the password has been changed
            QMessageBox.information(self, "Change Password", f"Password for {user_account} has been changed.")
        

    def cancel(self):
        # Importing MainUI inside the function to avoid a circular import
        from src.Dashboard import Dashboard  

        # Always create a new instance of the dashboard to avoid data leakage
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
