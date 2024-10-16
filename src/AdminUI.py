from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.uic import loadUi
import os
import sys
from PyQt5.QtCore import pyqtSlot

class AdminUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(AdminUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'AdminUI.ui')
        loadUi(ui_path, self)

        self.cancelButton.clicked.connect(self.cancel)

    def cancel(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
