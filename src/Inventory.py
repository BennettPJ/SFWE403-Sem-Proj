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
        self.initialize_csv(self.inventory_file, ['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'])
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
        """Read inventory data and return it as a list of dictionaries."""
        inventory_data = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    inventory_data.append({
                        'Item': row.get('Item', 'Unknown'),
                        'ID': row.get('ID', 'Unknown'),
                        'Quantity': row.get('Quantity', '0'),
                        'Price': row.get('Price', '0.00'),
                        'Expiration Date': row.get('Expiration Date', 'No Expiration Date'),
                        'Date Added': row.get('Date Added', ''),
                        'Date Updated': row.get('Date Updated', ''),
                        'Date Removed': row.get('Date Removed', '')
                    })
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


    def update_stock(self, item, item_id, new_quantity, price, expiration_date):
        """Update stock quantity and details for a specific item and ID."""
        rows = []
        updated = False
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Match the item and ID
                    if row['Item'].strip().lower() == item.strip().lower() and row['ID'].strip() == item_id.strip():
                        row['Quantity'] = str(new_quantity)
                        row['Price'] = price
                        row['Expiration Date'] = expiration_date
                        row['Date Updated'] = datetime.now().strftime('%Y-%m-%d')
                        updated = True
                    rows.append(row)

            if not updated:
                # Add new entry if not found
                rows.append({
                    'Item': item,
                    'ID': item_id,
                    'Quantity': str(new_quantity),
                    'Price': price,
                    'Expiration Date': expiration_date,
                    'Date Added': datetime.now().strftime('%Y-%m-%d'),
                    'Date Updated': '',
                    'Date Removed': ''
                })
                print(f"Added new entry: {item} with ID {item_id}, quantity {new_quantity}, price {price}")

            # Write back to CSV
            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'])
                writer.writeheader()
                writer.writerows(rows)
            print("Inventory file updated successfully.")
        except FileNotFoundError:
            print("Inventory file not found. Could not update stock.")

    def auto_order(self):
        """Automatically reorder items below the auto reorder threshold."""
        rows = []
        reorder_made = False
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if len(row) == 8:
                        item, item_id, quantity, price, exp_date, date_added, date_updated, date_removed = row
                        quantity = int(quantity)
                        
                        if quantity < self.auto_reorder_threshold:
                            reorder_amount = self.low_stock_threshold
                            quantity += reorder_amount
                            reorder_made = True
                            print(f"Reorder placed for {item} with new quantity {quantity}")
                        rows.append([item, item_id, str(quantity), price, exp_date, date_added, date_updated, date_removed])

            # Write updated quantities if reorder was made
            if reorder_made:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(rows)
                print("Reorder completed and inventory file updated.")
        except FileNotFoundError:
            print("Inventory file not found. No auto-order can be placed.")
        return reorder_made


    def check_low_stock(self):
        low_stock_items = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['Quantity']) < self.low_stock_threshold:
                        low_stock_items.append((row['Item'], row['ID'], row['Quantity']))
        except FileNotFoundError:
            print("Inventory file not found.")
        return low_stock_items


    def fill_prescription(self, item, quantity):
        """Deduct the specified quantity of an item from inventory, prioritizing earliest expiration date."""
        rows = []
        item_found = False
        remaining_quantity = quantity

        try:
            # Read current inventory data
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                inventory = [row for row in reader]

            # Filter and sort matching rows by expiration date
            matching_rows = [
                row for row in inventory
                if row['Item'].strip().lower() == item.strip().lower()
            ]
            matching_rows.sort(key=lambda x: datetime.strptime(x['Expiration Date'], '%Y-%m-%d'))

            if not matching_rows:
                print(f"{item} not found in inventory.")
                return False

            # Deduct stock
            for row in matching_rows:
                current_quantity = int(row['Quantity'])
                if current_quantity >= remaining_quantity:
                    row['Quantity'] = str(current_quantity - remaining_quantity)
                    remaining_quantity = 0
                    item_found = True
                    break
                else:
                    remaining_quantity -= current_quantity
                    row['Quantity'] = '0'

            if remaining_quantity > 0:
                print(f"Insufficient stock for {item}.")
                return False

            # Write updated inventory back to the file
            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'
                ])
                writer.writeheader()
                writer.writerows(inventory)

            return item_found

        except FileNotFoundError:
            print("Inventory file not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

            
    def check_exp_date(self):
        """Return items with expiration date within 30 days or already expired."""
        expiring_items = []
        today = datetime.today()
        threshold_date = today + timedelta(days=30)
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for item, item_id, quantity, price, exp_date, date_added, date_updated, date_removed in reader:
                    exp_date = exp_date.strip()
                    if exp_date != 'No Expiration Date':
                        exp_date_obj = datetime.strptime(exp_date, "%Y-%m-%d")
                        if exp_date_obj <= threshold_date:
                            expiring_items.append((item, item_id, quantity, exp_date))
        except FileNotFoundError:
            print("Inventory file not found. No expiring items to report.")
        return expiring_items


    def remove_medication(self, item_id):
        """Remove an item from the inventory by item_id."""
        rows = []
        item_found = False
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] != item_id:
                        rows.append(row)
                    else:
                        item_found = True

            if item_found:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'])
                    writer.writeheader()
                    writer.writerows(rows)
                print(f"Item with ID {item_id} removed successfully.")
            else:
                print(f"Item with ID {item_id} not found.")
            return item_found
        except FileNotFoundError:
            print("Inventory file not found.")
            return False
        
    def log_removal_activity(self, item, item_id, quantity, exp_date, employee_id):
        """Log the removal of an item in the activity log."""
        log_entry = {
            'Item': item,
            'ID': item_id,
            'Quantity': quantity,
            'Expiration Date': exp_date,
            'Employee ID': employee_id,
            'Removal Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(self.activity_file, mode='a', newline='') as log_file:
                writer = csv.DictWriter(log_file, fieldnames=log_entry.keys())
                if log_file.tell() == 0:
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