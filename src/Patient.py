import csv
import os

class Patient:
    def __init__(self, db_file='../DBFiles/db_patient_info.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(base_path, db_file)

        # Ensure the CSV file exists with headers
        if not os.path.exists(self.db_file):
            with open(self.db_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['FirstName', 'LastName', 'DateOfBirth', 'StreetAddress', 'City', 'State', 'ZipCode', 
                                 'PhoneNumber', 'Email', 'NameInsured', 'Provider', 'PolicyNumber', 'GroupNumber'])

    def add_patient(self, patient_data):
        """Adds a new patient record to the database."""
        with open(self.db_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                patient_data['FirstName'], patient_data['LastName'], patient_data['DateOfBirth'], 
                patient_data['StreetAddress'], patient_data['City'], patient_data['State'], 
                patient_data['ZipCode'], patient_data['PhoneNumber'], patient_data['Email'], 
                patient_data['NameInsured'], patient_data['Provider'], patient_data['PolicyNumber'], 
                patient_data['GroupNumber']
            ])
        print(f"Patient '{patient_data['FirstName']} {patient_data['LastName']}' added successfully.")

    def update_patient(self, first_name, last_name, dob, updated_data):
        """Updates a patient's information based on their name and date of birth."""
        rows = []
        updated = False

        with open(self.db_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['FirstName'] == first_name and row['LastName'] == last_name and row['DateOfBirth'] == dob:
                    for key, value in updated_data.items():
                        if key in row and value:
                            row[key] = value
                    updated = True
                rows.append(row)

        if updated:
            with open(self.db_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Patient '{first_name} {last_name}' updated successfully.")
        else:
            print("Patient not found.")
            
    def remove_patient(self, first_name, last_name, dob):
        """Removes a patient record based on their name and date of birth."""
        rows = []
        found = False

        with open(self.db_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['FirstName'] == first_name and row['LastName'] == last_name and row['DateOfBirth'] == dob:
                    found = True  # Mark as found, skip adding this row to keep it out of the new file
                else:
                    rows.append(row)  # Add non-matching rows to keep in the new file

        # Only rewrite the file if a matching record was found and removed
        if found:
            with open(self.db_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Patient '{first_name} {last_name}' removed successfully.")
            return True  # Return True to indicate a successful removal
        else:
            print("Patient not found.")
            return False  # Return False if no matching patient was found

    def find_patient(self, first_name, last_name, dob):
        """Finds and returns a patient's record based on their name and date of birth."""
        with open(self.db_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Strip whitespace from keys to ensure consistent access
                row = {key.strip(): value for key, value in row.items()}
                if row['FirstName'] == first_name and row['LastName'] == last_name and row['DateOfBirth'] == dob:
                    return row
        print("Patient not found.")
        return None