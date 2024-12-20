import csv
import os

class StoreInfoManager:
    def __init__(self, csv_file='../DBFiles/db_pharmacy_info.csv'): # Default file path
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.csv_file = os.path.join(base_path, csv_file)
        
        # Define the headers for the CSV file
        self.headers = [
            "name", "website", "address", "owner", "phone_number",
            "mon_hours", "tue_hours", "wed_hours", "thu_hours",
            "fri_hours", "sat_hours", "sun_hours"
            ]
        
        # Only initialize the CSV if it doesn’t already exist
        if not os.path.exists(self.csv_file):
            self._initialize_csv()

        # Load the current data from the CSV
        self.data = self._load_data()


    def _initialize_csv(self):
        # Write the headers to the CSV file
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            # Initialize with a row of empty values
            writer.writerow({header: "" for header in self.headers})


    def _load_data(self):
        # Read the first row of the CSV file
        with open(self.csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            # Return the first row if it exists, otherwise initialize with empty data
            return next(reader, {header: "" for header in self.headers})


    def get_info(self):
        # Return the in-memory data
        self.data = self._load_data()  # Refresh from file each time
        return self.data


    def update_info(self, field, value):
        # Update a single field in the CSV file
        self.data[field] = value  # Update in-memory dictionary
        
        # Write the updated data back to the CSV file
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()  # Write the header again
            writer.writerow(self.data)  # Write the single row of data
