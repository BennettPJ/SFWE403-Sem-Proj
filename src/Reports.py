#Reports.py
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
        """Display inventory data without removed items."""
        inventory_file = os.path.join(os.path.dirname(__file__), '..', 'DBFiles', 'db_inventory.csv')
        if os.path.exists(inventory_file):
            inventory_data = pd.read_csv(inventory_file)
            inventory_data['Quantity'] = pd.to_numeric(inventory_data['Quantity'], errors='coerce')

            # Replace NaN with blank
            inventory_data = inventory_data.fillna('')

            # Format dates to MM-DD-YYYY
            for date_col in ['Expiration Date', 'Date Added', 'Date Updated']:
                if date_col in inventory_data.columns:
                    inventory_data[date_col] = pd.to_datetime(
                        inventory_data[date_col], errors='coerce'
                    ).dt.strftime('%m-%d-%Y').fillna('')

            # Filter rows without 'Date Removed' and drop the column
            filtered_data = inventory_data[inventory_data['Date Removed'] == '']
            filtered_data = filtered_data.drop(columns=['Date Removed'], errors='ignore')

            # Rename columns with added spaces for better spacing
            filtered_data = filtered_data.rename(columns={
                
                'ID': ' ID    ',
                'Expiration Date': 'Expiration Date    ',
                'Date Added': 'Date Added    ',
                'Date Updated': 'Date Updated    ',
                'Quantity': 'Quantity    ',
                'Price': 'Price    '
            })

            # Generate report text with adjusted column spacing
            report_text = filtered_data.to_string(
                index=False,
                col_space=2  # Adjust column spacing for better readability
            ) if not filtered_data.empty else "No current inventory available."
            self.show_report_popup("Current Inventory Report", report_text)
        else:
            QMessageBox.warning(self, "File Not Found", "The inventory file could not be located.")

    def show_user_transactions(self):
        """Show user transaction logs for login/logout activity."""
        logs = self.read_log_file()
        formatted_logs = []

        if logs:
            for log in logs:
                try:
                    # Extract the date and rest of the log message
                    date_part, log_message = log.split(" - ", 1)
                    # Convert date to datetime object
                    log_datetime = datetime.strptime(date_part.split(",")[0], "%Y-%m-%d %H:%M:%S")
                    # Format the date as MM-DD-YYYY
                    formatted_date = log_datetime.strftime("%m-%d-%Y %I:%M:%S %p")
                    # Append the formatted log
                    formatted_logs.append(f"{formatted_date} - {log_message.strip()}")
                except ValueError:
                    # If log does not match expected format, append as is
                    formatted_logs.append(log.strip())

            # Combine formatted logs into a single string
            report_text = "\n".join(formatted_logs) if formatted_logs else "No login/logout activity found."
        else:
            report_text = "No log file found or it is empty."

        self.show_report_popup("User Transactions Report", report_text)


    def show_financial_report(self):
        """Show financial transactions from the logs."""
        logs = self.read_log_file()
        if logs:
            financial_logs = [log for log in logs if "purchase" in log.lower()]
            report_text = "\n".join(financial_logs) if financial_logs else "No financial transactions found."
        else:
            report_text = "No log file found or it is empty."

        self.show_report_popup("Financial Report", report_text)

    def show_inventory_report_for_period(self):
        """Generate inventory report for a specified period, including removed items."""
        start_date, end_date = self.get_date_range_from_user()
        if not (start_date and end_date):
            QMessageBox.warning(self, "Invalid Dates", "Please select a valid date range.")
            return

        inventory_file = os.path.join(os.path.dirname(__file__), '..', 'DBFiles', 'db_inventory.csv')
        if not os.path.exists(inventory_file):
            QMessageBox.warning(self, "File Not Found", "The inventory file could not be located.")
            return

        try:
            # Load inventory data
            inventory_data = pd.read_csv(inventory_file)

            # Convert 'Date Updated' to datetime and filter valid rows
            inventory_data['Date Updated'] = pd.to_datetime(
                inventory_data['Date Updated'], errors='coerce'
            )

            # Drop rows with invalid dates in 'Date Updated'
            inventory_data = inventory_data.dropna(subset=['Date Updated'])

            # Filter inventory by the selected date range
            filtered_data = inventory_data[
                (inventory_data['Date Updated'] >= pd.Timestamp(start_date)) &
                (inventory_data['Date Updated'] <= pd.Timestamp(end_date))
            ]

            # Replace NaN with blank in all columns
            filtered_data = filtered_data.fillna('')

            # Format dates in specific columns to MM-DD-YYYY
            for date_col in ['Expiration Date', 'Date Added', 'Date Updated', 'Date Removed']:
                if date_col in filtered_data.columns:
                    filtered_data[date_col] = pd.to_datetime(
                        filtered_data[date_col], errors='coerce'
                    ).dt.strftime('%m-%d-%Y').fillna('')

            # Rename columns with added spaces for better spacing
            filtered_data = filtered_data.rename(columns={
                
                'ID': ' ID    ',
                'Expiration Date': 'Expiration Date    ',
                'Date Added': 'Date Added    ',
                'Date Updated': 'Date Updated    ',
                'Quantity': 'Quantity    ',
                'Price': 'Price    '
            })

            # Prepare the report text
            report_text = filtered_data.to_string(index=False) if not filtered_data.empty else "No inventory updates found for the selected period."
            self.show_report_popup("Inventory Report for Period", report_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while processing the inventory report:\n{e}")

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

    def show_report_popup(self, title, report_text):
        """Display a report in a popup dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(900, 600)  # Increased popup window size

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
