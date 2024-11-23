# Import necessary libraries for system operations
import csv
import os
from LoginRoles import LoginRoles  
from datetime import datetime, timedelta

class Inventory:
    # Class constructor to initialize the inventory system, takes in the low stock threshold, auto reorder threshold, and paths to CSV databases
    def __init__(self, low_stock_threshold=120, auto_reorder_threshold=120, 
                 inventory_file='../DBFiles/db_inventory.csv'):
        
        # Set up the base directory path
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Ensure the 'DBFiles' directory exists, if not creates it 
        db_dir = os.path.join(base_path, 'DBFiles')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # Set the file paths relative to the base directory
        self.inventory_file = os.path.join(base_path, inventory_file)
        
        # Define thresholds for low stock and auto-reorder
        self.low_stock_threshold = low_stock_threshold
        self.auto_reorder_threshold = auto_reorder_threshold
        # Create an instance of the LoginRoles class
        self.login_roles = LoginRoles()  
        
        # Initialize CSV files with headers if they don't exist
        self.initialize_csv(self.inventory_file, ['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'])


    # Function to initialize a CSV file with headers if it does not exist
    def initialize_csv(self, file_path, headers):
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
    
    
    #Read inventory data and return it as a list of dictionaries
    def read_inventory_data(self):
        inventory_data = [] #initialize empty list to hold the values of the items 
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file) # Create a CSV DictReader for reading rows as dictionaries
                for row in reader:
                    #Append each row with default values if the data value is not found
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
        return inventory_data #returns the list 


    # Function displays the current stock from inventory in the table in the UI
    def view_stock(self):
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
        except FileNotFoundError:
            print("Inventory file not found. The inventory is currently empty.")


    # Function to update stock quantity and details for specific items and ID's
    def update_stock(self, item, item_id, new_quantity, price, expiration_date):
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

            # Add new item if it doesn't exist
            if not updated:
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

            # Write the updated data back to the inventory CSV
            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'])
                writer.writeheader()
                writer.writerows(rows)
        except FileNotFoundError:
            print("Inventory file not found. Could not update stock.")


    #Function to automatically reorder items if the items are below the threshold 
    def auto_order(self):
        rows = []
        reorder_made = False
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if len(row) == 8:
                        # Parse the row and check if it needs reordering
                        item, item_id, quantity, price, exp_date, date_added, date_updated, date_removed = row
                        quantity = int(quantity) #gets the quantity of the item 
                        
                        if quantity < self.auto_reorder_threshold: #checks if the quantity is less than the threshold, and reorders if necessary
                            reorder_amount = self.low_stock_threshold
                            quantity += reorder_amount
                            reorder_made = True
                        rows.append([item, item_id, str(quantity), price, exp_date, date_added, date_updated, date_removed])

            # Write updated quantities if reorder was made into inventory CSV
            if reorder_made:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(rows)
        except FileNotFoundError:
            print("Inventory file not found. No auto-order can be placed.")
        return reorder_made


    #Function to check what items are low in stock 
    def check_low_stock(self):
        low_stock_items = [] #empty list 
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file) # Create a CSV DictReader for reading rows as dictionaries
                for row in reader:
                    if int(row['Quantity']) < self.low_stock_threshold:
                        low_stock_items.append((row['Item'], row['ID'], row['Quantity']))
        except FileNotFoundError:
            print("Inventory file not found.")
        return low_stock_items #returns list of items found with low stock


    #Function updates the items quantity from inventory, prioritizing earliest expiration date
    def fill_prescription(self, item, quantity):
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

            # Updates stock in inventory
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

            # Write updated inventory back to the inventory CSV
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


    # Function to check items that are within 30 days to expire or have already expired    
    def check_exp_date(self):
        expiring_items = [] #empty list 
        today = datetime.today() #gets the current date
        threshold_date = today + timedelta(days=30) #threshold for time 30 days
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader) #skip header 
                for item, item_id, quantity, exp_date in reader:
                    exp_date = exp_date.strip()
                    if exp_date != 'No Expiration Date':
                        exp_date_obj = datetime.strptime(exp_date, "%Y-%m-%d") #gets the value of the expiration date of the item 
                        if exp_date_obj <= threshold_date: #checks if the date of the item is less than the threshold 
                            expiring_items.append((item, item_id, quantity, exp_date))
        except FileNotFoundError:
            print("Inventory file not found. No expiring items to report.")
        return expiring_items #returns list of items found that are less than the range expiration threshold


    # Function to remove an item from inventory based on their ID
    def remove_medication(self, item_id):
        rows = [] #empty list
        item_found = False
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file) # Create a CSV DictReader for reading rows as dictionaries
                for row in reader:
                    if row['ID'] != item_id: #Check for the item that is been removed. If is not the item it keeps it adds it to the list 
                        rows.append(row)
                    else:
                        item_found = True #target remove item found
            
            # Writes the inventory CSV without the item removed
            if item_found: 
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed']) #header
                    writer.writeheader() #adds the header to the csv
                    writer.writerows(rows)
            return item_found
        except FileNotFoundError:
            print("Inventory file not found.")
            return False
        
    
    # Function to check if an item that is been sell or prescribed is expired
    def is_expired(self, medication):
        today = datetime.today() #gets current date
        with open(self.inventory_file, mode='r') as file:
            reader = csv.DictReader(file) # Create a CSV DictReader for reading rows as dictionaries
            for row in reader:
                if row['Item'].strip().lower() == medication.strip().lower(): 
                    expiration_date = datetime.strptime(row['Expiration Date'], '%Y-%m-%d') #gets the item expiration date 
                    if expiration_date < today: #checks of the item has expired
                        return True
        return False
    
    
    #Function to retrieve all stock entries for a given item 
    def check_stock(self, medication):
        results = [] #empty list
        with open(self.inventory_file, mode='r') as file:
            reader = csv.DictReader(file) # Create a CSV DictReader for reading rows as dictionaries
            for row in reader:
                if row['Item'] == medication:
                    results.append({
                        'Medication': row['Item'],
                        'Quantity': int(row['Quantity']),
                        'Expiration Date': row['Expiration Date']
                    })
        if not results:
            raise ValueError(f"Medication '{medication}' not found in inventory.")
        return results #returns a list with all the current entries of the item in inventory