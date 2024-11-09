from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
import os
from PyQt5.uic import loadUi
from src.Patient import Patient  # Import the Patient class
from LoginRoles import LoginRoles

class PatientUI(QMainWindow):
    def __init__(self, widget, username):
        super(PatientUI, self).__init__()
        self.widget = widget
        self.username = username

        # Load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'UpdateCustomerInfo.ui')
        loadUi(ui_path, self)
        
        self.setMinimumSize(1000, 500)  # Set a minimum size
        self.cancelButton.clicked.connect(self.backToDashboard)
        self.savePatient.clicked.connect(self.savePatientInfo)
        self.updatePatient.clicked.connect(self.updatePatientInfo)
        self.removePatientButton.clicked.connect(self.removePatient)
        self.clear.clicked.connect(self.clearFields)
        
        # Initialize the Patient class to interact with the patient database
        self.patient_db = Patient()
        
        # Set up user role permissions
        self.setup_ui()
        
    def setup_ui(self):
        roles = LoginRoles()
        user_role = roles.find_user_role(self.username)
        # Only enable the remove button for managers or pharmacists
        self.removePatientButton.setEnabled(user_role in ['manager', 'pharmacist'])
        
    def backToDashboard(self):
        from src.Dashboard import Dashboard
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        
    def savePatientInfo(self):
        patient_data = {
            'FirstName': self.firstName.text(),
            'LastName': self.lastName.text(),
            'DateOfBirth': self.DOB.text(),
            'StreetAddress': self.address.text(),
            'City': self.city.text(),
            'State': self.state.text(),
            'ZipCode': self.zip.text(),
            'PhoneNumber': self.phoneNumber.text(),
            'Email': self.email.text(),
            'NameInsured': self.nameInsured.text(),
            'Provider': self.provider.text(),
            'PolicyNumber': self.policyNum.text(),
            'GroupNumber': self.groupNum.text()
        }

        existing_patient = self.patient_db.find_patient(
            patient_data['FirstName'],
            patient_data['LastName'],
            patient_data['DateOfBirth']
        )

        if existing_patient:
            self.patient_db.update_patient(
                patient_data['FirstName'],
                patient_data['LastName'],
                patient_data['DateOfBirth'],
                patient_data
            )
            QMessageBox.information(self, "Success", "Patient information updated successfully!")
        else:
            self.patient_db.add_patient(patient_data)
            QMessageBox.information(self, "Success", "New patient information saved successfully!")

    def updatePatientInfo(self):
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

    def prompt_retry(self):
        retry_dialog = QMessageBox(self)
        retry_dialog.setWindowTitle("Next Step")
        retry_dialog.setText("Would you like to try again or go back to Update Patient Info?")
        retry_dialog.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        retry_dialog.setDefaultButton(QMessageBox.Close)
        
        response = retry_dialog.exec_()
        
        if response == QMessageBox.Retry:
            self.removePatient()  # Retry patient removal
        elif response == QMessageBox.Close:
            self.returnToUpdatePatientInfo()  # Return to Update Patient Info page

    def returnToUpdatePatientInfo(self):
        self.widget.setCurrentIndex(self.widget.indexOf(self))

    def removePatient(self):
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

            if not first_name or not last_name or not dob:
                QMessageBox.warning(self, "Error", "All fields are required.")
                self.prompt_retry()
                return

            patient_exists = self.patient_db.find_patient(first_name, last_name, dob)
            if patient_exists:
                if self.patient_db.remove_patient(first_name, last_name, dob):
                    QMessageBox.information(self, "Success", "Patient information removed successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to remove patient.")
            else:
                QMessageBox.warning(self, "Error", "Patient not found.")
            
            self.prompt_retry()