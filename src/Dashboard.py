# dashboard.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime
from src.Purchases import Purchases
from src.PatientUI import PatientUI
from src.Reports import Reports
from FillPrescriptionUI import FillPrescriptionUI
from src.InventoryUI import InventoryUI
from src.OrderMedication import OrderMedication
from src.AdminUI import AdminUI
from LoginRoles import LoginRoles

class Dashboard(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
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
        self.MedButton.clicked.connect(self.goToMedication)
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
        roles = LoginRoles()
        user_role = roles.find_user_role(self.username)
        if user_role != 'manager':
            self.AdminButton.setEnabled(False)
            
        self.AdminButton.clicked.connect(self.goToAdmin)
        
        if user_role != 'pharmacist':
            self.fillPrescripButton.setEnabled(False)
            
        self.fillPrescripButton.clicked.connect(self.fillPrescription)

    def update_clock(self):
        current_time = QTime.currentTime()
        time_string = current_time.toString('hh:mm AP')
        self.clock.display(time_string)

    def logOutUser(self):
        from src.LogInGUI import MainUI

        # Remove any existing instance of MainUI to force re-rendering
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                self.widget.removeWidget(self.widget.widget(i))
                break  # Exit loop once the widget is removed

        # Create a new instance of MainUI
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
        self.widget.setFixedSize(800, 525)  # Set size to match the login screen

    def goToPurchases(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Purchases):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1169, 558)
                return

        purchases_screen = Purchases(self.widget, self.username)
        self.widget.addWidget(purchases_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(purchases_screen))
        self.widget.setFixedSize(1169, 558)

    def patientInfo(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), PatientUI):
                self.widget.removeWidget(self.widget.widget(i))
                break  # Exit loop once the widget is removed

        # Create a new instance of PatientUI
        patient_info = PatientUI(self.widget, self.username)
        self.widget.addWidget(patient_info)
        self.widget.setCurrentIndex(self.widget.indexOf(patient_info))
        self.widget.setFixedSize(1050, 600)  

    def goToReports(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Reports):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1000, 600)
                return

        reports_screen = Reports(self.widget, self.username)
        self.widget.addWidget(reports_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(reports_screen))
        self.widget.setFixedSize(1050, 600)

    def fillPrescription(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), FillPrescriptionUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1132, 661)
                return

        prescription_info = FillPrescriptionUI(self.widget, self.username)
        self.widget.addWidget(prescription_info)
        self.widget.setCurrentIndex(self.widget.indexOf(prescription_info))
        self.widget.setFixedSize(1132, 661)


    def goToInventoryUI(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), InventoryUI):
                self.widget.removeWidget(self.widget.widget(i))
                break  # Exit the loop as we found and removed the existing page
        
        # Create a new InventoryUI instance and add it to the widget
        inventory_screen = InventoryUI(self.widget, self.username)  # Pass both widget and username
        self.widget.addWidget(inventory_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(inventory_screen))
        self.widget.setFixedSize(1010, 500)
        

    def goToMedication(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), OrderMedication):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1050, 500)
                return

        medication_screen = OrderMedication(self.widget, self.username)  # Pass self.username as well
        self.widget.addWidget(medication_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(medication_screen))
        self.widget.setFixedSize(1050, 500)


    def goToAdmin(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), AdminUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(1000, 500)
                return

        admin_ui = AdminUI(self.widget, self.username)
        self.widget.addWidget(admin_ui)
        self.widget.setCurrentIndex(self.widget.indexOf(admin_ui))
        self.widget.setFixedSize(1050, 500)
