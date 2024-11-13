import csv
import os

class PendingPrescription:
    def __init__(self, pending_prescription_file='../DBFiles/db_pending_prescriptions.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.pending_file = os.path.join(base_path, pending_prescription_file)

        # Ensure the CSV file exists
        if not os.path.exists(self.pending_file):
            with open(self.pending_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Patient_First_Name', 'Patient_Last_Name', 'Patient_DOB', 'Prescription_Number', 'Medication', 'Quantity'])


    def add_prescription(self, first_name, last_name, dob, prescription_number, medication, quantity):
        """Add a new pending prescription to the database."""
        with open(self.pending_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, dob, prescription_number, medication, quantity])


    def read_prescriptions(self):
        """Read all prescriptions from the database."""
        with open(self.pending_file, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


    def update_prescription(self, prescription_number, updated_data):
        """
        Update a prescription based on the prescription number.
        :param prescription_number: Unique identifier of the prescription to update.
        :param updated_data: A dictionary with updated fields and their values.
        """
        prescriptions = self.read_prescriptions()
        updated = False

        with open(self.pending_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Patient_First_Name', 'Patient_Last_Name', 'Patient_DOB', 'Prescription_Number', 'Medication', 'Quantity'])
            writer.writeheader()

            for prescription in prescriptions:
                if prescription['Prescription_Number'] == prescription_number:
                    prescription.update(updated_data)
                    updated = True
                writer.writerow(prescription)

        return updated


    def delete_prescription(self, prescription_number):
        """
        Delete a prescription based on the prescription number.
        :param prescription_number: Unique identifier of the prescription to delete.
        """
        prescriptions = self.read_prescriptions()
        updated_prescriptions = [p for p in prescriptions if p['Prescription_Number'] != prescription_number]

        with open(self.pending_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Patient_First_Name', 'Patient_Last_Name', 'Patient_DOB', 'Prescription_Number', 'Medication', 'Quantity'])
            writer.writeheader()
            writer.writerows(updated_prescriptions)

        return len(updated_prescriptions) < len(prescriptions)
    
    
    def findByPatient(self, firstName, lastName, dob):
        prescriptions = self.read_prescriptions()
        return [p for p in prescriptions if p['Patient_First_Name'] == firstName and p['Patient_Last_Name'] == lastName and p['Patient_DOB'] == dob]