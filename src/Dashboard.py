# dashboard.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime
from Purchases import Purchases
from PatientUI import PatientUI
from Reports import Reports
from FillPrescriptionUI import FillPrescriptionUI
from InventoryUI import InventoryUI
from PrescriptionUI import PrescriptionUI
from AdminUI import AdminUI
from LoginRoles import LoginRoles

class Dashboard(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget and current username as an argument
        super(Dashboard, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.username = username  # Store the username

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Dashboard.ui')
        loadUi(ui_path, self)

        # Set fixed size for the dashboard
        self.widget.setFixedSize(1050, 600)

        # Ensure the logout button works
        self.logOut.clicked.connect(self.logOutUser)

        # Connect buttons to navigation functions
        self.purchase.clicked.connect(self.goToPurchases)
        self.ReportsButton.clicked.connect(self.goToReports)
        self.InventoryButton.clicked.connect(self.goToInventoryUI)
        self.fillPrescripButton.clicked.connect(self.fillPrescription)
        self.updatePatientInfoButton.clicked.connect(self.patientInfo)
        self.MedButton.clicked.connect(self.goToPendingPrescription)
        self.AdminButton.clicked.connect(self.goToAdmin)

        # Set QLCDNumber to handle 8 digits (HH:MM:SS)
        self.clock.setSegmentStyle(self.clock.Flat)
        self.clock.setDigitCount(8)

        # Set up a timer to update the clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Update every second

        # Initial clock display
        self.update_clock()
        
        # If not admin, disable admin button
        self.setup_ui()


    def setup_ui(self):
        self.AdminButton.setEnabled(True)  # Enable by default
        roles = LoginRoles() # Create an instance of the LoginRoles class
        user_role = roles.find_user_role(self.username) # Find the role of the current user
        if user_role != 'manager':
            #if the role isn't manager, disable the admin button
            self.AdminButton.setEnabled(False)
            
        # reconnect the button to the function
        self.AdminButton.clicked.connect(self.goToAdmin)
        
        if user_role != 'pharmacist':
            #if the role isn't pharmacist, disable the fill prescription button
            self.fillPrescripButton.setEnabled(False)
            
        # reconnect the button to the function
        self.fillPrescripButton.clicked.connect(self.fillPrescription)


    def update_clock(self):
        # Get the current time and format it as HH:MM AM/PM and display it
        current_time = QTime.currentTime()
        time_string = current_time.toString('hh:mm AP')
        self.clock.display(time_string)


    def logOutUser(self):
        from src.LogInGUI import MainUI #Don't want a circular import, so import here

        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                # Remove the widget so the screen updates if there is a new row
                self.widget.removeWidget(self.widget.widget(i)) 
                break  # Exit loop once the widget is removed

        # Create a new instance of MainUI
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
        self.widget.setFixedSize(800, 525)  # Set size to match the login screen


    def goToPurchases(self):
        # Check if the Purchases screen is already open
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Purchases):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1169, 558)
                return

        # If the Purchases screen is not open, create a new instance and add it to the widget
        purchases_screen = Purchases(self.widget, self.username)
        self.widget.addWidget(purchases_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(purchases_screen))
        self.widget.setFixedSize(1169, 558)


    def patientInfo(self):
        # Check if the PatientUI screen is already open
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), PatientUI):
                self.widget.removeWidget(self.widget.widget(i))
                break  # Exit loop once the widget is removed

        # If the PatientUI is not open, Create a new instance of PatientUI
        patient_info = PatientUI(self.widget, self.username)
        self.widget.addWidget(patient_info)
        self.widget.setCurrentIndex(self.widget.indexOf(patient_info))
        self.widget.setFixedSize(1050, 600)  


    def goToReports(self):
        # Check if the Reports screen is already open
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Reports):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1000, 600)
                return

        # If the Reports screen is not open, create a new instance and add it to the widget
        reports_screen = Reports(self.widget, self.username)
        self.widget.addWidget(reports_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(reports_screen))
        self.widget.setFixedSize(1050, 600)


    def fillPrescription(self):
        # Check if the FillPrescriptionUI screen is already open
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), FillPrescriptionUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1132, 661)
                return

        # If the FillPrescriptionUI is not open, Create a new instance of FillPrescriptionUI
        prescription_info = FillPrescriptionUI(self.widget, self.username)
        self.widget.addWidget(prescription_info)
        self.widget.setCurrentIndex(self.widget.indexOf(prescription_info))
        self.widget.setFixedSize(1132, 661)


    def goToInventoryUI(self):
        # Check if the InventoryUI screen is already open
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), InventoryUI):
                self.widget.removeWidget(self.widget.widget(i))
                break  # Exit the loop as we found and removed the existing page
        
        # Create a new InventoryUI instance and add it to the widget
        inventory_screen = InventoryUI(self.widget, self.username)  # Pass both widget and username
        self.widget.addWidget(inventory_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(inventory_screen))
        self.widget.setFixedSize(1010, 500)
        

    def goToPendingPrescription(self):
        # Check if the PrescriptionUI screen is already open
        #This is now prescription manager
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), PrescriptionUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1050, 500)
                return

        # If the PrescriptionUI is not open, Create a new instance of PrescriptionUI
        medication_screen = PrescriptionUI(self.widget, self.username)  # Pass self.username as well
        self.widget.addWidget(medication_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(medication_screen))
        self.widget.setFixedSize(1050, 500)


    def goToAdmin(self):
        # Check if the AdminUI screen is already open
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), AdminUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1000, 500)
                return

        # If the AdminUI is not open, Create a new instance of AdminUI
        admin_ui = AdminUI(self.widget, self.username)
        self.widget.addWidget(admin_ui)
        self.widget.setCurrentIndex(self.widget.indexOf(admin_ui))
        self.widget.setFixedSize(1050, 500)