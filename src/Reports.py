from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QDateEdit, QMessageBox, QHBoxLayout
from PyQt5.uic import loadUi
import os
from datetime import datetime
import pandas as pd

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
        self.inventoryReport.clicked.connect(self.show_inventory_report)
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

    def show_inventory_report(self):
        """Display inventory data with low stock items highlighted."""
        inventory_file = os.path.join(os.path.dirname(__file__), 'DBFiles', 'db_inventory.csv')
        
        # Load the inventory CSV
        if os.path.exists(inventory_file):
            inventory_data = pd.read_csv(inventory_file)
            
            # Ensure Quantity column is numeric
            inventory_data['Quantity'] = pd.to_numeric(inventory_data['Quantity'], errors='coerce')
            
            # Check for low stock items based on Quantity
            low_stock_items = inventory_data[inventory_data['Quantity'] < 5]  # Define low stock threshold
            
            # Display in a separate section
            if not low_stock_items.empty:
                low_stock_text = f"Low Stock Items:\n{low_stock_items.to_string(index=False)}\n"
            else:
                low_stock_text = "No low stock items found."
            
            report_text = low_stock_text
            self.show_report_popup("Inventory Report", report_text)
        else:
            QMessageBox.warning(self, "File Not Found", "The inventory file could not be located.")

    def show_user_transactions(self):
        logs = self.read_log_file()
        user_logs = [log for log in logs if "login" in log.lower() or "account" in log.lower()]
        self.show_report_popup("User Transactions Report", "\n".join(user_logs) if user_logs else "No records found.")

    def show_financial_report(self):
        logs = self.read_log_file()
        financial_logs = [log for log in logs if "purchase" in log.lower()]
        self.show_report_popup("Financial Report", "\n".join(financial_logs) if financial_logs else "No records found.")

    def show_inventory_report_for_period(self):
        """Generate inventory report for a specified period."""
        start_date, end_date = self.get_date_range_from_user()
        if start_date and end_date:
            logs = self.read_log_file()
            inventory_logs = [
                log for log in logs if "inventory" in log.lower() and self.is_within_date_range(log, start_date, end_date)
            ]
            self.show_report_popup("Inventory Report for Period", "\n".join(inventory_logs) if inventory_logs else "No records found.")

    def get_date_range_from_user(self):
        """Prompt the user to select a date range and return the start and end dates."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date Range")
        layout = QVBoxLayout(dialog)

        # Date selectors
        start_date_label = QLabel("Start Date:")
        self.start_date_edit = QDateEdit(calendarPopup=True)
        self.start_date_edit.setDate(datetime.now().date())
        
        end_date_label = QLabel("End Date:")
        self.end_date_edit = QDateEdit(calendarPopup=True)
        self.end_date_edit.setDate(datetime.now().date())

        # Set layout for date fields
        date_layout = QHBoxLayout()
        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_edit)

        layout.addLayout(date_layout)

        # Confirm button
        confirm_button = QPushButton("OK")
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button)

        if dialog.exec_() == QDialog.Accepted:
            start_date = self.start_date_edit.date().toPyDate()
            end_date = self.end_date_edit.date().toPyDate()
            return start_date, end_date
        return None, None

    def is_within_date_range(self, log, start_date, end_date):
        """Check if a log entry falls within the specified date range."""
        log_date = datetime.strptime(log.split(" - ")[0], "%Y-%m-%d")  # Adjust date parsing as per log format
        return start_date <= log_date <= end_date

    def show_report_popup(self, title, report_text):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout(dialog)
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setText(report_text if report_text else "No records found.")

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
