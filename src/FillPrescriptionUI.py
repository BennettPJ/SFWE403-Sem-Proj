#FillPrescription.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.uic import loadUi
from Patient import Patient
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
        self.FindPatient.clicked.connect(self.findPatient)
        self.fillPerscription.clicked.connect(self.fillPrescription)
        self.CheckStock.clicked.connect(self.checkStock)
        self.clear.clicked.connect(self.clearFields)
        
        self.patient_db = Patient()
        self.inventory_db = Inventory()
        
        
    def backToDashboard(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)
        
    def findPatient(self):
        # Create a dialog to search for a patient
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter Patient Information")
        dialog.setFixedSize(300, 200)
        layout = QVBoxLayout(dialog)

        firstNameInput = QLineEdit(dialog)
        firstNameInput.setPlaceholderText("First Name")
        layout.addWidget(QLabel("First Name"))
        layout.addWidget(firstNameInput)

        lastNameInput = QLineEdit(dialog)
        lastNameInput.setPlaceholderText("Last Name")
        layout.addWidget(QLabel("Last Name"))
        layout.addWidget(lastNameInput)

        dobInput = QLineEdit(dialog)
        dobInput.setPlaceholderText("Date of Birth (MM/DD/YYYY)")
        layout.addWidget(QLabel("Date of Birth"))
        layout.addWidget(dobInput)

        confirmButton = QPushButton("Confirm", dialog)
        layout.addWidget(confirmButton)
        confirmButton.clicked.connect(dialog.accept)

        if dialog.exec_() == QDialog.Accepted:
            first_name = firstNameInput.text().strip()
            last_name = lastNameInput.text().strip()
            dob = dobInput.text().strip()

            patient_data = self.patient_db.find_patient(first_name, last_name, dob)

            if patient_data:
                self.firstName.setText(patient_data['FirstName'])
                self.lastName.setText(patient_data['LastName'])
                self.DOB.setText(patient_data['DateOfBirth'])
                self.address.setText(patient_data['StreetAddress'])
                self.city.setText(patient_data['City'])
                self.state.setText(patient_data['State'])
                self.zip.setText(patient_data['ZipCode'])
                self.phoneNumber.setText(patient_data['PhoneNumber'])
                self.email.setText(patient_data['Email'])
                self.nameInsured.setText(patient_data['NameInsured'])
                self.provider.setText(patient_data['Provider'])
                self.policyNum.setText(patient_data['PolicyNumber'])
                self.groupNum.setText(patient_data['GroupNumber'])
                QMessageBox.information(self, "Success", "Patient information loaded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Patient not found.")

    def clearFields(self):
        self.firstName.clear()
        self.lastName.clear()
        self.DOB.clear()
        self.address.clear()
        self.city.clear()
        self.state.clear()
        self.zip.clear()
        self.phoneNumber.clear()
        self.email.clear()
        self.nameInsured.clear()
        self.provider.clear()
        self.policyNum.clear()
        self.groupNum.clear()
    
    def fillPrescription(self):
        try:
            print("Fill Prescription button clicked")

            # Check if the tableWidget widget exists
            if not hasattr(self, 'tableWidget'):
                print("Error: tableWidget widget is not available in the UI")
                QMessageBox.critical(self, "Error", "Prescription table not found in the UI.")
                return

            # Track if at least one prescription was processed successfully
            prescription_filled = False

            # Loop through each row in the prescription table
            for row in range(self.tableWidget.rowCount()):
                # Retrieve medication name and quantity from the table
                medication = self.tableWidget.item(row, 1).text() if self.tableWidget.item(row, 1) else ""
                quantity_str = self.tableWidget.item(row, 3).text() if self.tableWidget.item(row, 3) else ""

                print(f"Row {row}: Medication = {medication}, Quantity = {quantity_str}")

                if not medication or not quantity_str:
                    continue  # Skip empty rows
                
                # Check for expired medication
                if self.inventory_db.is_expired(medication):
                    QMessageBox.warning(self, "Error", f"Cannot fill prescription: {medication} is expired.")
                    continue  # Skip filling expired medication

                try:
                    quantity = int(quantity_str)
                except ValueError:
                    QMessageBox.warning(self, "Error", f"Invalid quantity for {medication}. Please enter a numeric value.")
                    return

                # Call the backend to fill the prescription and update inventory
                success = self.inventory_db.fill_prescription(medication, quantity)
                print(f"Success status for {medication}: {success}")

                if success:
                    prescription_filled = True
                    QMessageBox.information(self, "Prescription Filled", f"Filled {quantity} units of {medication}. Inventory updated.")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to fill prescription for {medication}. Insufficient stock or medication not found.")

            # If at least one prescription was filled, clear the table
            if prescription_filled:
                self.clearPrescriptionTable()

        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while filling the prescription: {e}")

    def clearPrescriptionTable(self):
        """Clears all rows in the prescription table."""
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row, column, QTableWidgetItem(""))  # Set each cell to an empty string



        
    def checkStock(self):
        pass
    
    
    