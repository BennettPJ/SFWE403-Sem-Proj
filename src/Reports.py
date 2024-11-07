from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QDateEdit, QMessageBox
from PyQt5.uic import loadUi
import os
from datetime import datetime

class Reports(QMainWindow):
    def __init__(self, widget, username):  
        super(Reports, self).__init__()
        self.widget = widget  
        self.username = username  

        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Reports.ui')
        loadUi(ui_path, self)

        self.setMinimumSize(900, 600)

        # Connect existing buttons
        self.cancelButton.clicked.connect(self.cancelPurchase)
        self.inventoryReport.clicked.connect(self.show_inventory_updates)
        self.userTransactionsReport.clicked.connect(self.show_user_transactions)

        # New buttons (Add in Designer)
        self.financialReportButton = QPushButton("Financial Report")  
        self.financialReportButton.clicked.connect(self.show_financial_report)

        self.inventoryTimeReportButton = QPushButton("Inventory Report for Period")  
        self.inventoryTimeReportButton.clicked.connect(self.show_inventory_report_for_period)

    def read_log_file(self):
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'transaction.log')
        if not os.path.exists(log_file):
            return []
        with open(log_file, 'r') as file:
            return file.readlines()

    def show_inventory_updates(self):
        logs = self.read_log_file()
        inventory_logs = [log for log in logs if "inventory" in log.lower()]
        self.show_report_popup("Inventory Updates Report", inventory_logs)

    def show_user_transactions(self):
        logs = self.read_log_file()
        user_logs = [log for log in logs if "login" in log.lower() or "account" in log.lower()]
        self.show_report_popup("User Transactions Report", user_logs)

    def show_financial_report(self):
        logs = self.read_log_file()
        financial_logs = [log for log in logs if "purchase" in log.lower()]
        self.show_report_popup("Financial Report", financial_logs)  # Adjust to add totals as needed

    def show_inventory_report_for_period(self):
        """Generate inventory report for a specified period."""
        start_date, end_date = self.get_date_range()
        logs = self.read_log_file()
        inventory_logs = [
            log for log in logs if "inventory" in log.lower() and self.is_within_date_range(log, start_date, end_date)
        ]
        self.show_report_popup("Inventory Report for Period", inventory_logs)

    def get_date_range(self):
        """Display date selection popup and get the selected date range."""
        # Implement date selection using QDateEdit fields or similar in UI
        start_date = datetime(2024, 1, 1)  # Replace with actual user input
        end_date = datetime(2024, 12, 31)  # Replace with actual user input
        return start_date, end_date

    def is_within_date_range(self, log, start_date, end_date):
        """Check if a log entry falls within the specified date range."""
        log_date = datetime.strptime(log.split(" - ")[0], "%Y-%m-%d")  # Adjust date parsing as per log format
        return start_date <= log_date <= end_date

    def show_report_popup(self, title, logs):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout(dialog)
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setText("\n".join(logs) if logs else "No records found.")

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)

        layout.addWidget(log_display)
        layout.addWidget(close_button)

        dialog.exec_()

    def cancelPurchase(self):
        from src.Dashboard import Dashboard  
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
