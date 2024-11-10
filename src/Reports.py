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

        # Load the UI
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Reports.ui')
        loadUi(ui_path, self)

        self.setMinimumSize(900, 600)

        # Connect existing buttons
        self.cancelButton.clicked.connect(self.cancelPurchase)
        self.inventoryReport.clicked.connect(self.show_inventory_report)
        self.userTransactionsReport.clicked.connect(self.show_user_transactions)
        self.financialReportButton.clicked.connect(self.show_financial_report)
        self.inventoryTimeReportButton.clicked.connect(self.show_inventory_report_for_period)

    def read_log_file(self):
        """Read the transaction log file."""
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'transaction.log')
        if not os.path.exists(log_file):
            return []
        with open(log_file, 'r') as file:
            return file.readlines()

    def show_inventory_report(self):
        """Display inventory data with low stock items highlighted."""
        inventory_file = os.path.join(os.path.dirname(__file__), 'DBFiles', 'db_inventory.csv')
        if os.path.exists(inventory_file):
            inventory_data = pd.read_csv(inventory_file)
            inventory_data['Quantity'] = pd.to_numeric(inventory_data['Quantity'], errors='coerce')
            low_stock_items = inventory_data[inventory_data['Quantity'] < 5]

            report_text = "Low Stock Items:\n" + (low_stock_items.to_string(index=False) if not low_stock_items.empty else "No low stock items found.")
            self.show_report_popup("Inventory Report", report_text)
        else:
            QMessageBox.warning(self, "File Not Found", "The inventory file could not be located.")

    def show_user_transactions(self):
        """Show user transaction logs for login/logout activity."""
        logs = self.read_log_file()
        user_logs = [log for log in logs if "login" in log.lower() or "logout" in log.lower()]
        report_text = "\n".join(user_logs) if user_logs else "No user transactions found."
        self.show_report_popup("User Transactions Report", report_text)

    def show_financial_report(self):
        """Show financial transactions from the logs."""
        logs = self.read_log_file()
        financial_logs = [log for log in logs if "purchase" in log.lower()]
        report_text = "\n".join(financial_logs) if financial_logs else "No financial transactions found."
        self.show_report_popup("Financial Report", report_text)

    def show_inventory_report_for_period(self):
        """Generate inventory report for a specified period."""
        start_date, end_date = self.get_date_range_from_user()
        if not (start_date and end_date):
            QMessageBox.warning(self, "Invalid Dates", "Please select a valid date range.")
            return

        logs = self.read_log_file()
        inventory_logs = [log for log in logs if "inventory" in log.lower() and self.is_within_date_range(log, start_date, end_date)]
        report_text = "\n".join(inventory_logs) if inventory_logs else "No inventory records found for the selected period."
        self.show_report_popup("Inventory Report for Period", report_text)

    def get_date_range_from_user(self):
        """Prompt the user to select a date range."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date Range")
        layout = QVBoxLayout(dialog)

        start_date_label = QLabel("Start Date:")
        self.start_date_edit = QDateEdit(calendarPopup=True)
        self.start_date_edit.setDate(datetime.now().date())

        end_date_label = QLabel("End Date:")
        self.end_date_edit = QDateEdit(calendarPopup=True)
        self.end_date_edit.setDate(datetime.now().date())

        date_layout = QHBoxLayout()
        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_edit)

        layout.addLayout(date_layout)

        confirm_button = QPushButton("OK")
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button)

        if dialog.exec_() == QDialog.Accepted:
            start_date = self.start_date_edit.date().toPyDate()
            end_date = self.end_date_edit.date().toPyDate()
            return start_date, end_date
        return None, None

    def is_within_date_range(self, log, start_date, end_date):
        """Check if a log entry falls within a date range."""
        log_date_str = log.split(" - ")[0]
        try:
            log_date = datetime.strptime(log_date_str, "%Y-%m-%d")
            return start_date <= log_date <= end_date
        except ValueError:
            return False

    def show_report_popup(self, title, report_text):
        """Display a report in a popup dialog."""
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
        """Return to the dashboard."""
        from src.Dashboard import Dashboard
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
