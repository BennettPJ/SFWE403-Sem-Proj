#FillPrescription.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class FillPrescriptionUI(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
        super(FillPrescriptionUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.username = username

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'FillPrescription.ui')
        loadUi(ui_path, self)
        
            # Set a minimum size for the dashboard
        self.setMinimumSize(1000, 600)  # Example size, you can adjust these values
        
        self.cancelButton.clicked.connect(self.cancelOrder)
        
    def cancelOrder(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))