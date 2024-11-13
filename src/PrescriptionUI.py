from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5.uic import loadUi
import os
import sys
from PyQt5.QtCore import pyqtSlot
from Prescriptions import Prescriptions

class PrescriptionUI(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
        super(PrescriptionUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.username = username  # Store the username

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'PendingPrescription.ui')
        loadUi(ui_path, self)
                # Set a minimum size for the dashboard
        self.setMinimumSize(900, 500)
        self.cancelButton.clicked.connect(self.backButton)
        self.addPrescription.clicked.connect(self.addPrescriptionToDB)
        self.FindPrescriptionsPatient.clicked.connect(self.findPatient)
        self.clearTable.clicked.connect(self.reset_table)
        self.pickUp.clicked.connect(self.pickUpPrescription)
        
        self.pending_prescription_db = Prescriptions()
        

    def backButton(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Reset the table before returning to the dashboard.
        self.reset_table()

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))

    def addPrescriptionToDB(self):
        firstName = self.PatientFirstName.text().strip()
        lastName = self.PatientLastName.text().strip()
        date_of_birth = self.PatientDOB.text().strip()
        prescription_number = self.PrescriptionNumber.text().strip()
        medication = self.Medication.text().strip()
        quantity = self.Quantity.text().strip()
        
        if not all([firstName, lastName, date_of_birth, prescription_number, medication, quantity]):
            QMessageBox.warning(self, "Warning", "Please fill all fields.")
            return
        
        # Add the prescription to the database
        self.pending_prescription_db.add_prescription(firstName, lastName, date_of_birth, prescription_number, medication, quantity)
        
        #show success message
        success_popup = QMessageBox()
        success_popup.setIcon(QMessageBox.Information)
        success_popup.setWindowTitle("Success")
        success_popup.setText("Prescription added successfully!")
        success_popup.exec_()
        
        # Clear the fields after adding the prescription
        self.PatientFirstName.clear()
        self.PatientLastName.clear()
        self.PatientDOB.clear()
        self.PrescriptionNumber.clear()
        self.Medication.clear()
        self.Quantity.clear()

    def reset_table(self):
        """Clear all items from the ItemsTable while keeping the rows."""
        for row in range(self.ItemsTable.rowCount()):
            for column in range(self.ItemsTable.columnCount()):
                self.ItemsTable.setItem(row, column, QTableWidgetItem(""))  # Clear the cell contents
                
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
            
            # Retrieve prescriptions for the patient
            patient_prescription_data = self.pending_prescription_db.findByPatient(first_name, last_name, dob)

            # Set the table widget's row count to the number of entries found
            self.ItemsTable.setRowCount(len(patient_prescription_data))
            self.ItemsTable.setColumnCount(len(self.pending_prescription_db.read_prescriptions()[0]))

            # Populate the table
            for row_index, row_data in enumerate(patient_prescription_data):
                for col_index, value in enumerate(row_data.values()):  # Use row_data.values() to get dictionary values
                    self.ItemsTable.setItem(row_index, col_index, QTableWidgetItem(str(value)))
                    
    def pickUpPrescription(self):
        """Change the status of the selected prescription to Picked Up."""
        # Get the selected row
        selected_row = self.ItemsTable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "No row selected. Please select a prescription to pick up.")
            return

        # Retrieve the Prescription Number from the selected row
        prescription_number_item = self.ItemsTable.item(selected_row, 3)  # Assuming the 4th column is Prescription_Number
        if prescription_number_item is None:
            QMessageBox.warning(self, "Warning", "Invalid selection. Please select a valid row.")
            return

        prescription_number = prescription_number_item.text()

        # Call the database method to update the status
        success = self.pending_prescription_db.pickup_prescription(prescription_number)

        if success:
            # Update the status in the UI
            self.ItemsTable.setItem(selected_row, 6, QTableWidgetItem("Picked Up"))  # Assuming the 7th column is Status

            # Show success message
            QMessageBox.information(self, "Success", f"Prescription {prescription_number} marked as Picked Up.")
        else:
            # Show error message
            QMessageBox.warning(self, "Error", "Failed to update the prescription. Please try again.")