import csv
import os
from LoginRoles import LoginRoles  # Import the LoginRoles class
from datetime import datetime, timedelta

class Inventory:
    def __init__(self, low_stock_threshold=120, auto_reorder_threshold=120, activity_file='../DBFiles/db_inventory_activity_log.csv',inventory_file='../DBFiles/db_inventory.csv'):
        # Set up the base directory path
        base_path = os.path.dirname(os.path.abspath(__file__))
        print(f"Base path: {base_path}")

        # Ensure the 'DBFiles' directory exists, if not, create it
        db_dir = os.path.join(base_path, 'DBFiles')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # Set the file paths relative to the base directory
        self.inventory_file = os.path.join(base_path, inventory_file)
        self.activity_file = os.path.join(base_path, activity_file)
        #print(f"Inventory file path: {self.inventory_file}") #debug purpose 

        # Ensure the inventory file exists, and create it if necessary
        self.ensure_inventory_file_exists()

        self.low_stock_threshold = low_stock_threshold
        self.auto_reorder_threshold = auto_reorder_threshold
        self.login_roles = LoginRoles()  # Create an instance of the LoginRoles class
        
        # Ensure the inventory CSV file exists and has the correct header
        self.initialize_csv(self.inventory_file, ['Medication', 'ID', 'Quantity', 'Expiration Date'])
        #Ensure the activity CSV file exists and has the correct header
        self.initialize_csv(self.activity_file, ['Medication','ID','Quantity','Expiration Date', 'ID Employee', 'Removal Date'])

    def initialize_csv(self, file_path, headers):
        """Helper method to initialize a CSV file with headers if it does not exist."""
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)


    def ensure_inventory_file_exists(self):
        """Ensure that the inventory file exists. If not, create the file with a header row."""
        if not os.path.isfile(self.inventory_file):
            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Medication', 'ID', 'Quantity', 'Expiration Date'])  # Write the header
    
    
    def read_inventory_data(self):
        """Read inventory data from CSV file and return as a list of dictionaries."""
        inventory_data = []
        
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    inventory_data.append({
                        'Medication': row.get('Medication', 'Unknown'),
                        'ID': row.get('ID', 'Unknown'),
                        'Quantity': row.get('Quantity', '0'),
                        'Expiration Date': row.get('Expiration Date', 'No Expiration Date')
                    })
            #print(f"Successfully read inventory data: {inventory_data}")
        except FileNotFoundError:
            print(f"Inventory file not found: {self.inventory_file}")
        return inventory_data


    def view_stock(self):
        """Display the current stock in the inventory."""
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                stock_empty = True
                print("Current inventory stock:")
                for medication, item_id, quantity, exp_date in reader:
                    stock_empty = False
                    print(f"{medication} (ID: {item_id}): {quantity} units, Expiration Date: {exp_date}")
                if stock_empty:
                    print("The inventory is currently empty.")
        except FileNotFoundError:
            print("Inventory file not found. The inventory is currently empty.")


    def update_stock(self, medication, new_id, new_quantity, expiration_date):
        """
        Updates the stock for a specific medication. If a row with the same
        medication name and ID exists, it is replaced with the new quantity and expiration date.
        Otherwise, it adds a new entry.
        """
        rows = []
        updated = False

        try:
            # Read the current inventory file
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # If the medication and ID match, update this row's quantity and expiration date
                    if row['Medication'].strip().lower() == medication.strip().lower() and row['ID'].strip() == new_id.strip():
                        row['Quantity'] = str(new_quantity)
                        row['Expiration Date'] = expiration_date
                        updated = True
                    # Retain each row in the list
                    rows.append(row)

            # If the medication wasn't found, add it as a new entry
            if not updated:
                rows.append({
                    'Medication': medication,
                    'ID': new_id,
                    'Quantity': str(new_quantity),
                    'Expiration Date': expiration_date
                })
                print(f"Added new entry: {medication} with ID {new_id}: {new_quantity} units, Expiration Date: {expiration_date}")

            # Write the updated inventory back to the file
            with open(self.inventory_file, mode='w', newline='') as file:
                fieldnames = ['Medication', 'ID', 'Quantity', 'Expiration Date']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print("Inventory file updated successfully.")

        except FileNotFoundError:
            print("Inventory file not found. Creating a new inventory.")
            # If file is not found, create it with the updated row
            with open(self.inventory_file, mode='w', newline='') as file:
                fieldnames = ['Medication', 'ID', 'Quantity', 'Expiration Date']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    'Medication': medication,
                    'ID': new_id,
                    'Quantity': str(new_quantity),
                    'Expiration Date': expiration_date
                })
            print("New inventory file created and updated successfully.")


    def auto_order(self):
        """Automatically reorder items if their quantity is below the auto reorder threshold."""
        rows = []
        reorder_made = False  # Track if any reorder occurs

        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if len(row) == 4:
                        medication, item_id, quantity, exp_date = row
                        quantity = int(quantity)
                        
                        # Check if below threshold and if reorder needed
                        if quantity < self.auto_reorder_threshold:
                            reorder_amount = self.low_stock_threshold  # Add this fixed amount
                            quantity += reorder_amount
                            reorder_made = True  # Set reorder_made to True only if a reorder is placed
                            print(f"Reorder placed for {medication} with new quantity {quantity}")
                        rows.append([medication, item_id, str(quantity), exp_date])

            # Write back the updated quantities if any reorder happened
            if reorder_made:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(rows)
                print("Reorder made and inventory file updated.")

        except FileNotFoundError:
            print("Inventory file not found. No auto-order can be placed.")
            return False

        print(f"Reorder made status: {reorder_made}")
        return reorder_made  # Return if reorder occurred


    def check_low_stock(self):
        """Check for items with stock below the low stock threshold and display alerts."""
        low_stock_items = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for medication, item_id, quantity, exp_date in reader:
                    if int(quantity) < self.low_stock_threshold:
                        low_stock_items.append((medication, item_id, quantity, exp_date))

            return low_stock_items
        except FileNotFoundError:
            print("Inventory file not found. No low stock medications to report.")
            return []


    def fill_prescription(self, medication, quantity):
        """Deduct the specified quantity of a medication from inventory, prioritizing earliest expiration date."""
        rows = []
        medication_found = False
        remaining_quantity = quantity

        try:
            # Read current inventory data
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                inventory = [row for row in reader]

            # Filter and sort matching rows by expiration date (earliest first)
            matching_rows = [
                row for row in inventory
                if row['Item'].strip().lower() == medication.strip().lower()
            ]
            matching_rows.sort(key=lambda x: datetime.strptime(x['Expiration Date'], '%Y-%m-%d'))

            if not matching_rows:
                print(f"{medication} not found in inventory.")
                return False  # Medication not found

            # Deduct stock from the matching rows
            for row in matching_rows:
                current_quantity = int(row['Quantity'])
                if current_quantity >= remaining_quantity:
                    row['Quantity'] = str(current_quantity - remaining_quantity)
                    remaining_quantity = 0
                    medication_found = True
                    print(f"Filled {quantity} units of {medication}. Remaining in this batch: {row['Quantity']}")
                    break  # Fully filled
                else:
                    remaining_quantity -= current_quantity
                    row['Quantity'] = '0'
                    print(f"Used {current_quantity} units of {medication} from batch with expiration {row['Expiration Date']}.")

            # Check if the prescription was fully filled
            if remaining_quantity > 0:
                print(f"Insufficient stock for {medication}. Unable to fill {remaining_quantity} units.")
                return False

            # Write the updated inventory back to the CSV
            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'])
                writer.writeheader()
                writer.writerows(inventory)

            return medication_found

        except FileNotFoundError:
            print("Inventory file not found.")
            return False
        except Exception as e:
            print(f"An error occurred while filling prescription: {e}")
            return False

            
    def check_exp_date(self):
        """Check for items with expiration date within 30 days or already expired."""
        expiring_items = []
        today = datetime.today()
        threshold_date = today + timedelta(days=30)  # Date 30 days from today

        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for medication, item_id, quantity, exp_date in reader:
                    exp_date = exp_date.strip()  # Remove leading/trailing whitespace
                    if exp_date != 'No Expiration Date':
                        # Convert exp_date from string to datetime
                        exp_date_obj = datetime.strptime(exp_date, "%m/%d/%Y")
                        
                        # Check if the expiration date is past or within 30 days from today
                        if exp_date_obj <= threshold_date:
                            expiring_items.append((medication, item_id, quantity, exp_date))

            return expiring_items
        except FileNotFoundError:
            print("Inventory file not found. No expiring medications to report.")
            return []


    def remove_medication(self, item_id):
        """Removes an item from the inventory by item_id and updates the CSV file."""
        rows = []
        item_found = False
        
        try:
            # Step 1: Read current inventory data
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Check if the current row matches the item_id to delete
                    if row['ID'] == item_id:
                        item_found = True  # Mark that we found and will remove this item
                        print(f"Found and removing item with ID: {item_id}")
                        continue  # Skip this row, effectively removing it from the list
                    rows.append(row)  # Keep all other rows

            # Step 2: Write back to the CSV if the item was found
            if item_found:
                with open(self.inventory_file, mode='w', newline='') as file:
                    fieldnames = ['Medication', 'ID', 'Quantity', 'Expiration Date']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)  # Write all rows except the deleted one
                print(f"Item with ID {item_id} removed successfully.")
                return True
            else:
                print(f"Item with ID {item_id} not found in inventory.")
                return False

        except FileNotFoundError:
            print("Inventory file not found.")
            return False
        
    def log_removal_activity(self, medication, item_id, quantity, exp_date, employee_id):
        """
        Logs the removal of an item in the activity log database.
        """
        log_entry = {
            'Medication': medication,
            'ID': item_id,
            'Quantity': quantity,
            'Expiration Date': exp_date,
            'ID Employee': employee_id,
            'Removal Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Open the activity log in append mode
            with open(self.activity_file, mode='a', newline='') as log_file:
                writer = csv.DictWriter(log_file, fieldnames=log_entry.keys())
                if log_file.tell() == 0:  # Write headers if file is new
                    writer.writeheader()
                writer.writerow(log_entry)
            print("Removal action logged successfully.")
        except Exception as e:
            print(f"Error logging removal: {e}")
    
    def is_expired(self, medication):
        """Check if the given medication is expired."""
        today = datetime.today()
        with open(self.inventory_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Item'].strip().lower() == medication.strip().lower():  # Use 'Item' instead of 'Medication'
                    expiration_date = datetime.strptime(row['Expiration Date'], '%Y-%m-%d')
                    if expiration_date < today:
                        return True
        return False
    
    
    def check_stock(self, medication):
        """Retrieve all stock entries for a given medication."""
        results = []
        with open(self.inventory_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Item'] == medication:
                    results.append({
                        'Medication': row['Item'],
                        'Quantity': int(row['Quantity']),
                        'Expiration Date': row['Expiration Date']
                    })
        if not results:
            raise ValueError(f"Medication '{medication}' not found in inventory.")
        return results