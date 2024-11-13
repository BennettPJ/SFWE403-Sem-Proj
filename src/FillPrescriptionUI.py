#FillPrescription.py
import sys
import os
from datetime import datetime

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.uic import loadUi
from Prescriptions import Prescriptions
from Inventory import Inventory


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
        
        self.cancelButton.clicked.connect(self.backToDashboard)
        self.fillPerscription.clicked.connect(self.fillPrescription)
        self.CheckStock.clicked.connect(self.checkStock)
        self.Refresh.clicked.connect(self.refreshTable)

        self.prescriptions_db = Prescriptions()
        self.inventory_db = Inventory()
        
        # Load the inventory database
        self.initializeTable()
        
        
    def initializeTable(self):
        # Query the database for all pending prescriptions
        pending_prescriptions = [p for p in self.prescriptions_db.read_prescriptions() if p['Status'] == 'Pending']

        # Set the table's row count to the number of pending prescriptions
        self.tableWidget.setRowCount(len(pending_prescriptions))

        # Populate the table with data
        for row_index, prescription in enumerate(pending_prescriptions):
            for col_index, value in enumerate(prescription.values()):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))
    
    
    def backToDashboard(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)
    
    
    def fillPrescription(self):
        """Fill the selected prescription if it is not expired and update its status."""
        try:
            # Get the selected row
            selected_row = self.tableWidget.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Warning", "No row selected. Please select a prescription to fill.")
                return

            # Retrieve the medication name, quantity, and prescription number from the selected row
            medication_item = self.tableWidget.item(selected_row, 4)  
            quantity_item = self.tableWidget.item(selected_row, 5) 
            prescription_number_item = self.tableWidget.item(selected_row, 3) 

            if not medication_item or not quantity_item or not prescription_number_item:
                QMessageBox.warning(self, "Warning", "Incomplete data in the selected row.")
                return

            medication = medication_item.text().strip()
            try:
                quantity = int(quantity_item.text().strip())
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid quantity. Please enter a valid number.")
                return

            prescription_number = prescription_number_item.text().strip()

            # Check if the medication is expired
            if self.inventory_db.is_expired(medication):
                QMessageBox.warning(self, "Warning", f"The medication '{medication}' is expired and cannot be dispensed.")
                return

            # Attempt to fill the prescription
            success = self.inventory_db.fill_prescription(medication, quantity)

            if success:
                # Update the prescription status in the database
                status_updated = self.prescriptions_db.update_status(prescription_number, "Filled")

                if status_updated:
                    QMessageBox.information(self, "Success", f"Successfully filled {quantity} units of '{medication}'. Prescription status updated.")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to update status for prescription {prescription_number}.")

                self.refreshTable()  # Refresh the table to reflect updated data
            else:
                QMessageBox.warning(self, "Error", f"Failed to fill the prescription for '{medication}'. Insufficient stock or medication not found.")

        except Exception as e:
            print(f"An error occurred while filling the prescription: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while filling the prescription: {e}")


    def checkStock(self):
        """Check the stock of the medication for the selected prescription."""
        # Get the selected row
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "No row selected. Please select a prescription to check stock.")
            return

        # Retrieve the medication name from the selected row (assume column 4 is the medication name)
        medication_item = self.tableWidget.item(selected_row, 4)  # Adjust column index if needed
        if not medication_item:
            QMessageBox.warning(self, "Warning", "Medication name not found in the selected row.")
            return

        medication = medication_item.text()

        # Check the stock from the inventory database
        try:
            stock_entries = self.inventory_db.check_stock(medication)
            if stock_entries:
                # Create a string to display all entries
                message = f"Stock information for {medication}:\n\n"
                for entry in stock_entries:
                    message += f"Quantity: {entry['Quantity']}, Expiration Date: {entry['Expiration Date']}\n"
                QMessageBox.information(self, "Stock Information", message)
            else:
                QMessageBox.warning(self, "Warning", f"No stock information found for {medication}.")

        except Exception as e:
            print(f"An error occurred while checking stock: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while checking stock: {e}")
    
    
    def refreshTable(self):
        """
        Populates the table with prescriptions that have a status of 'Pending'.
        """
        try:
            # Clear the table before refreshing
            self.tableWidget.clearContents()

            # Query the database for all pending prescriptions
            pending_prescriptions = [p for p in self.prescriptions_db.read_prescriptions() if p['Status'] == 'Pending']

            # Set the table's row count to the number of pending prescriptions
            self.tableWidget.setRowCount(len(pending_prescriptions))

            # Populate the table with data
            for row_index, prescription in enumerate(pending_prescriptions):
                for col_index, value in enumerate(prescription.values()):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

            QMessageBox.information(self, "Success", f"Loaded {len(pending_prescriptions)} pending prescriptions.")

        except Exception as e:
            print(f"An error occurred while refreshing the table: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while refreshing the table: {e}")
        
    
    