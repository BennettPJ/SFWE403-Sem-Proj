import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime
from src.Purchases import Purchases
from src.CustomerInfo import CustomerInfo
from src.Reports import Reports
from src.FillPrescription import FillPrescriptionUI
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
        
        #If not admin disable admin button
        self.setup_ui()
        
    def setup_ui(self):
        self.AdminButton.setEnabled(True) #Enable by default
        roles = LoginRoles()
        userRole = roles.find_user_role(self.username)
        if userRole != 'manager':
            self.AdminButton.setEnabled(False)
            
        self.AdminButton.clicked.connect(self.goToAdmin)

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

            """ Navigate to the Purchases page """
            # Check if the purchases page is already in the stack
            for i in range(self.widget.count()):
                if isinstance(self.widget.widget(i), Purchases):
                    self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                    return

            # If not in the stack, create a new instance of Purchases and add it to the stack
            purchases_screen = Purchases(self.widget, self.username)
            self.widget.addWidget(purchases_screen)
            self.widget.setCurrentIndex(self.widget.indexOf(purchases_screen))
            self.widget.setFixedSize(1169, 558)
    def updateCustomerInfo(self):
                    # Check if the purchases page is already in the stack
            for i in range(self.widget.count()):
                if isinstance(self.widget.widget(i), CustomerInfo):
                    self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                    return
                
            # If not in the stack, create a new instance of Purchases and add it to the stack
            customerInfo = CustomerInfo(self.widget, self.username)
            self.widget.addWidget(customerInfo)
            self.widget.setCurrentIndex(self.widget.indexOf(customerInfo))
        
    def goToReports(self):
            """ Navigate to the Reports page """
            # Check if the purchases page is already in the stack
            for i in range(self.widget.count()):
                if isinstance(self.widget.widget(i), Reports):
                    self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                    return

            # If not in the stack, create a new instance of Purchases and add it to the stack
            reports_screen = Reports(self.widget, self.username)
            self.widget.addWidget(reports_screen)
            self.widget.setCurrentIndex(self.widget.indexOf(reports_screen))

    def fillPrescription(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), FillPrescriptionUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return


        # If not in the stack, create a new instance of Purchases and add it to the stack
        prescripInfo = FillPrescriptionUI(self.widget, self.username)
        self.widget.addWidget(prescripInfo)
        self.widget.setCurrentIndex(self.widget.indexOf(prescripInfo))
        self.widget.setFixedSize(1132, 661)


    def goToInventoryUI(self):
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), InventoryUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        inventory_screen = InventoryUI(self.widget, self.username)  # Pass both widget and username
        self.widget.addWidget(inventory_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(inventory_screen))
        self.widget.setFixedSize(1010, 500)



    def goToMedication(self):
        # Check if the purchases page is already in the stack

        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), OrderMedication):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        medication_screen = OrderMedication(self.widget)
        self.widget.addWidget(medication_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(medication_screen))

    def goToAdmin(self):

        # If not in the stack, create a new instance of Purchases and add it to the stack
        prescripInfo = OrderMedication(self.widget, self.username)
        self.widget.addWidget(prescripInfo)
        self.widget.setCurrentIndex(self.widget.indexOf(prescripInfo))

    def goToAdmin(self):       
        # Check if the purchases page is already in the stack

        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), AdminUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return


        # If not in the stack, create a new instance of Purchases and add it to the stack
        admin_ui = AdminUI(self.widget, self.username)
        self.widget.addWidget(admin_ui)
        self.widget.setCurrentIndex(self.widget.indexOf(admin_ui))

