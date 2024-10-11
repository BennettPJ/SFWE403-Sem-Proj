#CustomerInfo.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class CustomerInfo(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(CustomerInfo, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'UpdateCustomerInfo.ui')
        loadUi(ui_path, self)
        
        self.cancelButton.clicked.connect(self.cancelPurchase)
        
    def cancelPurchase(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))