#Reports.py
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QDateEdit, QMessageBox, QHBoxLayout
from PyQt5.uic import loadUi
import os
from datetime import datetime
import pandas as pd
import csv
from fpdf import FPDF
import tempfile
import webbrowser


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

    def export_to_csv(self, data, report_name):
        """Export the report data to a CSV file."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{report_name}_{current_date}.csv"
        file_path = os.path.join(os.path.dirname(__file__), '..', 'Reports', file_name)

        # Ensure the Reports directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Export data to CSV
        data.to_csv(file_path, index=False)
        QMessageBox.information(self, "Export Successful", f"{report_name} has been exported to {file_path}.")



    def show_inventory_report(self):
        """
        Generate a PDF inventory report and display it.
        """
        inventory_file = os.path.join(os.path.dirname(__file__), '..', 'DBFiles', 'db_inventory.csv')
        if not os.path.exists(inventory_file):
            QMessageBox.warning(self, "File Not Found", "The inventory file could not be located.")
            return

        # Load and filter inventory data
        inventory_data = pd.read_csv(inventory_file)
        filtered_data = inventory_data[inventory_data['Date Removed'].isnull() | (inventory_data['Date Removed'] == '')]

        # Drop the 'Date Removed' column
        if 'Date Removed' in filtered_data.columns:
            filtered_data = filtered_data.drop(columns=['Date Removed'])

        # Format dates for readability
        for date_col in ['Expiration Date', 'Date Added', 'Date Updated']:
            if date_col in filtered_data.columns:
                filtered_data[date_col] = pd.to_datetime(
                    filtered_data[date_col], errors='coerce'
                ).dt.strftime('%m-%d-%Y').fillna('')

        # Generate the PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        # Add a title
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, txt="Inventory Report", ln=True, align='C')
        pdf.ln(10)

        # Define column headers and relative widths
        headers = ['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated']
        col_relative_widths = [2, 1, 1, 1, 2, 2, 2]  # Adjust these relative weights
        total_width = sum(col_relative_widths)
        page_width = 190  # Approximate usable width for A4
        col_widths = [page_width * (w / total_width) for w in col_relative_widths]

        # Add the table headers
        pdf.set_font("Arial", style='B', size=10)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C')
        pdf.ln()

        # Add table rows
        pdf.set_font("Arial", size=10)
        for _, row in filtered_data.iterrows():
            pdf.cell(col_widths[0], 10, str(row['Item']), border=1)
            pdf.cell(col_widths[1], 10, str(row['ID']), border=1, align='C')
            pdf.cell(col_widths[2], 10, str(row['Quantity']), border=1, align='C')
            pdf.cell(col_widths[3], 10, f"{row['Price']:.2f}", border=1, align='C')
            pdf.cell(col_widths[4], 10, row['Expiration Date'], border=1, align='C')
            pdf.cell(col_widths[5], 10, row['Date Added'], border=1, align='C')
            pdf.cell(col_widths[6], 10, row['Date Updated'], border=1, align='C')
            pdf.ln()

        # Save the PDF to a temporary file
        temp_pdf_path = os.path.join(tempfile.gettempdir(), "Inventory_Report.pdf")
        pdf.output(temp_pdf_path)

        # Open the PDF in the default viewer
        webbrowser.open(temp_pdf_path)



    def show_user_transactions(self):
        """
        Generate a PDF report for user login/logout activity.
        """
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
                    formatted_logs.append({"Date": formatted_date, "Log Message": log_message.strip()})
                except ValueError:
                    # If log does not match expected format, append as is
                    formatted_logs.append({"Date": "", "Log Message": log.strip()})

            # Generate the PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Add title
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, txt="User Transactions Report", ln=True, align='C')
            pdf.ln(10)

            # Add table headers
            headers = ['Date', 'Log Message']
            col_widths = [60, 120]  # Adjust these widths as needed
            pdf.set_font("Arial", style='B', size=10)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, border=1, align='C')
            pdf.ln()

            # Add table rows
            pdf.set_font("Arial", size=10)
            for log in formatted_logs:
                pdf.cell(col_widths[0], 10, str(log['Date']), border=1, align='C')
                pdf.cell(col_widths[1], 10, str(log['Log Message']), border=1, align='L')
                pdf.ln()

            # Save the PDF to a temporary file
            temp_pdf_path = os.path.join(tempfile.gettempdir(), "User_Transactions_Report.pdf")
            pdf.output(temp_pdf_path)

            # Open the PDF in the default viewer
            webbrowser.open(temp_pdf_path)

        else:
            QMessageBox.warning(self, "No Data", "No log file found or it is empty.")


    def show_financial_report(self):
        """
        Generate a financial report for a specified date range and display it as a PDF.
        """
        purchase_file = os.path.join(os.path.dirname(__file__), '..', 'DBFiles', 'db_purchase_data.csv')

        if not os.path.exists(purchase_file):
            QMessageBox.warning(self, "File Not Found", "The purchase data file could not be located.")
            return

        # Prompt user to select a date range
        start_date, end_date = self.get_date_range_from_user()
        if not (start_date and end_date):
            QMessageBox.warning(self, "Invalid Dates", "Please select a valid date range.")
            return

        try:
            # Read purchase data
            purchase_data = pd.read_csv(purchase_file)
            purchase_data['Date'] = pd.to_datetime(purchase_data['Date'], errors='coerce')

            # Filter by date range
            filtered_data = purchase_data[
                (purchase_data['Date'] >= pd.Timestamp(start_date)) & 
                (purchase_data['Date'] <= pd.Timestamp(end_date))
            ]

            if filtered_data.empty:
                QMessageBox.information(self, "No Data", "No financial transactions found for the selected period.")
                return

            # Generate the PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Add title
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, txt="Financial Report", ln=True, align='C')
            pdf.ln(10)

            # Add summary
            total_revenue = filtered_data['Total Cost'].sum()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Total Revenue: ${total_revenue:.2f}", ln=True, align='L')
            pdf.ln(5)

            # Add table headers
            headers = ['Date', 'Item Name', 'Total Cost', 'Payment Method']
            col_widths = [40, 50, 40, 60]
            pdf.set_font("Arial", style='B', size=10)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, border=1, align='C')
            pdf.ln()

            # Add table rows
            pdf.set_font("Arial", size=10)
            for _, row in filtered_data.iterrows():
                pdf.cell(col_widths[0], 10, str(row['Date']), border=1, align='C')
                pdf.cell(col_widths[1], 10, str(row['Item Name']), border=1, align='C')
                pdf.cell(col_widths[2], 10, f"${row['Total Cost']:.2f}", border=1, align='C')
                pdf.cell(col_widths[3], 10, str(row['Payment Method']), border=1, align='C')
                pdf.ln()

            # Save the PDF to a temporary file
            temp_pdf_path = os.path.join(tempfile.gettempdir(), "Financial_Report.pdf")
            pdf.output(temp_pdf_path)

            # Open the PDF in the default viewer
            webbrowser.open(temp_pdf_path)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the financial report:\n{e}")

    def show_inventory_report_for_period(self):
        """
        Generate a PDF inventory report for a specified period and display it.
        """
        start_date, end_date = self.get_date_range_from_user()
        if not (start_date and end_date):
            QMessageBox.warning(self, "Invalid Dates", "Please select a valid date range.")
            return

        inventory_file = os.path.join(os.path.dirname(__file__), '..', 'DBFiles', 'db_inventory.csv')
        if not os.path.exists(inventory_file):
            QMessageBox.warning(self, "File Not Found", "The inventory file could not be located.")
            return

        try:
            # Load and filter inventory data
            inventory_data = pd.read_csv(inventory_file)
            inventory_data['Date Updated'] = pd.to_datetime(inventory_data['Date Updated'], errors='coerce')
            inventory_data['Date Removed'] = pd.to_datetime(inventory_data['Date Removed'], errors='coerce')

            filtered_data = inventory_data[
                (inventory_data['Date Updated'] >= pd.Timestamp(start_date)) & 
                (inventory_data['Date Updated'] <= pd.Timestamp(end_date))
            ]

            if filtered_data.empty:
                QMessageBox.information(self, "No Data", "No inventory updates found for the selected period.")
                return

            # Remove the time portion from 'Date Updated' and 'Date Removed'
            filtered_data['Date Updated'] = filtered_data['Date Updated'].dt.strftime('%m-%d-%Y')
            filtered_data['Date Removed'] = filtered_data['Date Removed'].dt.strftime('%m-%d-%Y').fillna('')

            # Generate the PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Add title
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, txt="Inventory Report for Period", ln=True, align='C')
            pdf.ln(10)

            # Add table headers
            headers = ['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed']
            col_relative_widths = [2, 1, 1, 1, 2, 2, 2, 2]  # Adjust these relative weights
            total_width = sum(col_relative_widths)
            page_width = 190  # Approximate usable width for A4
            col_widths = [page_width * (w / total_width) for w in col_relative_widths]

            pdf.set_font("Arial", style='B', size=10)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, border=1, align='C')
            pdf.ln()

            # Add table rows
            pdf.set_font("Arial", size=10)
            for _, row in filtered_data.iterrows():
                pdf.cell(col_widths[0], 10, str(row['Item']), border=1)
                pdf.cell(col_widths[1], 10, str(row['ID']), border=1, align='C')
                pdf.cell(col_widths[2], 10, str(row['Quantity']), border=1, align='C')
                pdf.cell(col_widths[3], 10, f"${row['Price']:.2f}", border=1, align='C')
                pdf.cell(col_widths[4], 10, str(row['Expiration Date']), border=1, align='C')
                pdf.cell(col_widths[5], 10, str(row['Date Added']), border=1, align='C')
                pdf.cell(col_widths[6], 10, str(row['Date Updated']), border=1, align='C')
                pdf.cell(col_widths[7], 10, str(row['Date Removed']), border=1, align='C')
                pdf.ln()

            # Save the PDF to a temporary file
            temp_pdf_path = os.path.join(tempfile.gettempdir(), "Inventory_Report_Period.pdf")
            pdf.output(temp_pdf_path)

            # Open the PDF in the default viewer
            webbrowser.open(temp_pdf_path)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the inventory report:\n{e}")




    def generate_financial_report(file_path):
        try:
            # Data structures to hold the aggregated data
            total_revenue = 0.0
            revenue_by_item = defaultdict(float)
            revenue_by_payment = defaultdict(float)
            transactions = []

            # Read the CSV file
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Extract relevant data
                    item_name = row['Item Name']
                    payment_method = row['Payment Method']
                    total_cost = float(row['Total Cost'])
                    grand_total = float(row['Grand Total'])

                    # Update totals
                    total_revenue += total_cost
                    revenue_by_item[item_name] += total_cost
                    revenue_by_payment[payment_method] += grand_total
                    transactions.append(row)

            # Generate and print the report
            print("\n--- Financial Report ---")
            print(f"Total Revenue: ${total_revenue:.2f}\n")

            # Revenue by item
            print("--- Revenue by Item ---")
            item_table = PrettyTable(['Item Name', 'Revenue'])
            for item, revenue in revenue_by_item.items():
                item_table.add_row([item, f"${revenue:.2f}"])
            print(item_table)

            # Revenue by payment method
            print("\n--- Revenue by Payment Method ---")
            payment_table = PrettyTable(['Payment Method', 'Revenue'])
            for method, revenue in revenue_by_payment.items():
                payment_table.add_row([method, f"${revenue:.2f}"])
            print(payment_table)

            # Transaction details
            print("\n--- Transaction Details ---")
            transaction_table = PrettyTable(['Date', 'First Name', 'Last Name', 'Grand Total', 'Payment Method'])
            for transaction in transactions:
                transaction_table.add_row([
                    transaction['Date'],
                    transaction['First Name'],
                    transaction['Last Name'],
                    f"${transaction['Grand Total']}",
                    transaction['Payment Method']
                ])
            print(transaction_table)

        except Exception as e:
            print(f"Error generating financial report: {e}")

    # File path to the CSV file
    csv_file_path = 'db_purchase_data.csv'

    # Generate the report
    generate_financial_report(csv_file_path)


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