import csv
import os

class Prescriptions:
    def __init__(self, prescription_file='../DBFiles/db_prescriptions.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.prescription_file = os.path.join(base_path, prescription_file)

        # Ensure the CSV file exists
        if not os.path.exists(self.prescription_file):
            with open(self.prescription_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Patient_First_Name', 'Patient_Last_Name', 'Patient_DOB', 'Prescription_Number', 'Medication', 'Quantity', 'Status'])


    def add_prescription(self, first_name, last_name, dob, prescription_number, medication, quantity):
        """Add a new pending prescription to the database."""
        with open(self.prescription_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, dob, prescription_number, medication, quantity, 'Pending'])


    def read_prescriptions(self):
        """Read all prescriptions from the database."""
        with open(self.prescription_file, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    
    
    def findByPatient(self, firstName, lastName, dob):
        prescriptions = self.read_prescriptions()
        return [p for p in prescriptions if p['Patient_First_Name'] == firstName and p['Patient_Last_Name'] == lastName and p['Patient_DOB'] == dob]
    
    
    def pickup_prescription(self, prescription_number):
        """Mark the prescription as picked up by updating its status."""
        prescriptions = self.read_prescriptions()
        updated = False

        # Update the status of the prescription
        for p in prescriptions:
            if p['Prescription_Number'] == prescription_number:
                p['Status'] = 'Picked Up'
                updated = True
                break

        # Write the updated prescriptions back to the CSV file
        with open(self.prescription_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Patient_First_Name', 'Patient_Last_Name', 'Patient_DOB',
                                                      'Prescription_Number', 'Medication', 'Quantity', 'Status'])
            writer.writeheader()
            writer.writerows(prescriptions)

        return updated
    
    
    def update_status(self, prescription_number, new_status):
        """Update the status of a prescription in the database."""
        prescriptions = self.read_prescriptions()
        updated = False

        # Update the status of the selected prescription
        for p in prescriptions:
            if p['Prescription_Number'] == prescription_number:
                p['Status'] = new_status
                updated = True
                break

        # Write back to the CSV
        if updated:
            with open(self.prescription_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Patient_First_Name', 'Patient_Last_Name', 'Patient_DOB',
                                                        'Prescription_Number', 'Medication', 'Quantity', 'Status'])
                writer.writeheader()
                writer.writerows(prescriptions)

        return updated