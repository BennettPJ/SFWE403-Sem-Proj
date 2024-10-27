import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime
from src.Purchases import Purchases
from src.CustomerInfo import CustomerInfo
from src.Reports import Reports
from src.FillPrescription import FillPrescriptionUI
from src.InventoryUI import InventoryUI
from src.OrderMedication import OrderMedication
from src.AdminUI import AdminUI

class Dashboard(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(Dashboard, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        
    
        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Dashboard.ui')
        loadUi(ui_path, self)

        # Set fixed size for the dashboard
        self.setFixedSize(1050, 600)

        # Ensure the logout button works
        self.logOut.clicked.connect(self.logOutUser)

        # Connect buttons to navigation functions
        self.purchase.clicked.connect(self.goToPurchases)
        self.ReportsButton.clicked.connect(self.goToReports)
        self.InventoryButton.clicked.connect(self.goToInventoryUI)
        self.fillPrescripButton.clicked.connect(self.fillPrescription)
        self.updateCustomerInfoButton.clicked.connect(self.updateCustomerInfo)
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

    def update_clock(self):
        current_time = QTime.currentTime()
        time_string = current_time.toString('hh:mm AP')
        self.clock.display(time_string)

    def logOutUser(self):
        from src.LogInGUI import MainUI

        # Check if the login screen already exists in the stack
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                self.widget.setFixedSize(800, 525)  # Resize to match the login screen size
                return

        # If not in the stack, create a new instance of MainUI and add it to the stack
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
        self.widget.setFixedSize(800, 525)  # Resize to match login screen size

    def goToPurchases(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Purchases):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        purchases_screen = Purchases(self.widget)
        self.widget.addWidget(purchases_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(purchases_screen))
        self.widget.setFixedSize(1169, 558)

    def updateCustomerInfo(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), CustomerInfo):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        customer_info = CustomerInfo(self.widget)
        self.widget.addWidget(customer_info)
        self.widget.setCurrentIndex(self.widget.indexOf(customer_info))

    def goToReports(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Reports):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        reports_screen = Reports(self.widget)
        self.widget.addWidget(reports_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(reports_screen))

    def fillPrescription(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), FillPrescriptionUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        prescription_screen = FillPrescriptionUI(self.widget)
        self.widget.addWidget(prescription_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(prescription_screen))
        self.widget.setFixedSize(1132, 661)

    def goToInventoryUI(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), InventoryUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        inventory_screen = InventoryUI(self.widget)
        self.widget.addWidget(inventory_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(inventory_screen))
        self.widget.setFixedSize(1010, 500)

    def goToMedication(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), OrderMedication):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        medication_screen = OrderMedication(self.widget)
        self.widget.addWidget(medication_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(medication_screen))

    def goToAdmin(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), AdminUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        admin_screen = AdminUI(self.widget)
        self.widget.addWidget(admin_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(admin_screen))
