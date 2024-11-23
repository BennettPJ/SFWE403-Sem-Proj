from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QInputDialog,QLabel
from PyQt5.uic import loadUi
import os
from PyQt5.QtCore import QTimer, QTime

from src.LoginRoles import LoginRoles
from src.StoreInfoManager import StoreInfoManager

class StoreHoursUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(StoreHoursUI, self).__init__()
        self.widget = widget
        
        # Instantiate StoreInfoManager
        self.info_manager = StoreInfoManager()


        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'storeHours.ui')
        loadUi(ui_path, self)

        # Set the window title
        self.widget.setFixedSize(1000, 500)
        
        # Set QLCDNumber to handle 8 digits (HH:MM:SS)
        self.lcdNumber.setSegmentStyle(self.lcdNumber.Flat)
        self.lcdNumber.setDigitCount(8)

        # Set up a timer to update the clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Update every second

        # Initial clock display
        self.update_clock()
        
        # Take the label input and store it in the variable
        self.label_pharmacy_name = self.findChild(QLabel, "label_pharmacy_name")
        self.label_pharmacy_website = self.findChild(QLabel, "label_pharmacy_website")
        self.label_pharmacy_address = self.findChild(QLabel, "label_pharmacy_address")
        self.label_pharmacy_owner = self.findChild(QLabel, "label_pharmacy_owner")
        self.label_pharmacy_phone = self.findChild(QLabel, "label_pharmacy_phone")

        self.label_monday_hours = self.findChild(QLabel, "label_monday_hours")
        self.label_tuesday_hours = self.findChild(QLabel, "label_tuesday_hours")
        self.label_wednesday_hours = self.findChild(QLabel, "label_wednesday_hours")
        self.label_thursday_hours = self.findChild(QLabel, "label_thursday_hours")
        self.label_friday_hours = self.findChild(QLabel, "label_friday_hours")
        self.label_saturday_hours = self.findChild(QLabel, "label_saturday_hours")
        self.label_sunday_hours = self.findChild(QLabel, "label_sunday_hours")
                
        # Load the initial pharmacy info from CSV into labels
        self.load_pharmacy_info()
        
        # Connect the buttons to their respective functions
        self.backBtn.clicked.connect(self.back_to_login) 
        self.hoursUpdateBtn.clicked.connect(self.update_store_hours)
        
    
    def update_clock(self):
        # Update the clock display with the current time
        current_time = QTime.currentTime()
        time_string = current_time.toString('hh:mm AP')
        self.lcdNumber.display(time_string)
        
        
    def load_pharmacy_info(self):
        # Get the pharmacy information from the CSV
        data = self.info_manager.get_info()

        # Set label text with CSV data
        self.label_pharmacy_name.setText(f"Pharmacy Name: {data['name']}")
        self.label_pharmacy_website.setText(f"Pharmacy Website: {data['website']}")
        self.label_pharmacy_address.setText(f"Pharmacy Address: {data['address']}")
        self.label_pharmacy_owner.setText(f"Pharmacy Owner: {data['owner']}")
        self.label_pharmacy_phone.setText(f"Pharmacy Phone Number: {data['phone_number']}")

        # Set each day's hours
        self.label_monday_hours.setText(f"Monday: {data['mon_hours']}")
        self.label_tuesday_hours.setText(f"Tuesday: {data['tue_hours']}")
        self.label_wednesday_hours.setText(f"Wednesday: {data['wed_hours']}")
        self.label_thursday_hours.setText(f"Thursday: {data['thu_hours']}")
        self.label_friday_hours.setText(f"Friday: {data['fri_hours']}")
        self.label_saturday_hours.setText(f"Saturday: {data['sat_hours']}")
        self.label_sunday_hours.setText(f"Sunday: {data['sun_hours']}")
        
        
    def back_to_login(self):
        # Go back to the login screen
        from src.LogInGUI import MainUI  # Import MainUI inside the function to avoid circular import

        # Check if MainUI (login screen) is already in the stack to avoid duplicates
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                self.widget.setCurrentIndex(i)
                self.widget.setFixedSize(800, 525)
                return

        # If not found, create a new MainUI instance
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
        self.widget.setFixedSize(800, 525)  
        

    def update_store_hours(self):
        # Authenticate the manager since they are the only ones that can make changes
        manager_username, ok = QInputDialog.getText(self, "Manager Approval", "Enter Manager Username:")
        if not ok or not manager_username:
            QMessageBox.warning(self, "Update Cancelled", "Manager approval is required to update store hours.")
            return

        manager_password, ok = QInputDialog.getText(self, "Manager Approval", "Enter Manager Password:", QLineEdit.Password)
        if not ok or not manager_password:
            QMessageBox.warning(self, "Update Cancelled", "Manager approval is required to update store hours.")
            return

        # Verify manager credentials
        roles = LoginRoles()
        success, message = roles.login(manager_username, manager_password)
        if not success or roles.find_user_role(manager_username) != 'manager':
            QMessageBox.warning(self, "Authorization Failed", "Manager approval failed. Please try again.")
            return

        # Update the pharmacy information
        fields = {
            "Pharmacy Name": ("name", self.label_pharmacy_name),
            "Pharmacy Website": ("website", self.label_pharmacy_website),
            "Pharmacy Address": ("address", self.label_pharmacy_address),
            "Pharmacy Owner": ("owner", self.label_pharmacy_owner),
            "Pharmacy Phone Number": ("phone_number", self.label_pharmacy_phone),
        }

        for field_name, (csv_field, label) in fields.items():
            new_value, ok = QInputDialog.getText(self, "Update Pharmacy Info", f"Enter {field_name} (Leave blank to skip):")
            if ok and new_value:  # Only update if the user provided a new value
                label.setText(f"{field_name}: {new_value}")
                self.info_manager.update_info(csv_field, new_value)

        days = {
            "Monday": ("mon_hours", self.label_monday_hours),
            "Tuesday": ("tue_hours", self.label_tuesday_hours),
            "Wednesday": ("wed_hours", self.label_wednesday_hours),
            "Thursday": ("thu_hours", self.label_thursday_hours),
            "Friday": ("fri_hours", self.label_friday_hours),
            "Saturday": ("sat_hours", self.label_saturday_hours),
            "Sunday": ("sun_hours", self.label_sunday_hours),
        }

        for day, (csv_field, label) in days.items():
            hours, ok = QInputDialog.getText(self, "Update Pharmacy Info", f"Enter {day} Working Hours (Leave blank to skip):")
            if ok and hours:  # Only update if the user provided new hours
                label.setText(f"{day}: {hours}")
                self.info_manager.update_info(csv_field, hours)

        # Reload labels to ensure display reflects the updated CSV
        self.load_pharmacy_info()
        QMessageBox.information(self, "Success", "Pharmacy information and store hours updated successfully!")