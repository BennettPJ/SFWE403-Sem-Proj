# Inventory.py
import csv
import os
from datetime import datetime, timedelta
from LoginRoles import LoginRoles


class Inventory:
    def __init__(self, inventory_file='../DBFiles/db_inventory.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.inventory_file = os.path.join(base_path, inventory_file)
        self.low_stock_threshold = 120
        self.auto_reorder_threshold = 120
        self.ensure_inventory_file_exists()

    def ensure_inventory_file_exists(self):
        if not os.path.isfile(self.inventory_file):
            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(
                    file, fieldnames=['Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed']
                )
                writer.writeheader()

    def read_inventory_data(self):
        inventory_data = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    inventory_data.append({
                        'Item': row.get('Item', ''),
                        'ID': row.get('ID', ''),
                        'Quantity': row.get('Quantity', ''),
                        'Price': row.get('Price', ''),
                        'Expiration Date': row.get('Expiration Date', ''),
                        'Date Added': row.get('Date Added', ''),
                        'Date Updated': row.get('Date Updated', ''),
                        'Date Removed': row.get('Date Removed', '')
                    })
        except FileNotFoundError:
            print("Inventory file not found.")
        return inventory_data

    def update_stock(self, item, item_id, quantity, exp_date, price=None):
        rows = []
        current_date = datetime.now().strftime('%Y-%m-%d')
        updated = False

        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Item'] == item and row['ID'] == item_id:
                        row['Quantity'] = str(quantity)
                        row['Price'] = price or row['Price']
                        row['Expiration Date'] = exp_date
                        row['Date Updated'] = current_date
                        updated = True
                    rows.append(row)

            if not updated:
                rows.append({
                    'Item': item,
                    'ID': item_id,
                    'Quantity': str(quantity),
                    'Price': price or "0.00",
                    'Expiration Date': exp_date,
                    'Date Added': current_date,
                    'Date Updated': current_date,
                    'Date Removed': ''
                })

            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'
                ])
                writer.writeheader()
                writer.writerows(rows)

        except FileNotFoundError:
            print("Inventory file not found.")
    def remove_item(self, item, item_id):
        """
        Mark an item as removed by adding a 'Date Removed' value instead of deleting it.
        """
        rows = []
        current_date = datetime.now().strftime('%Y-%m-%d')
        removed = False

        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Item'] == item and row['ID'] == item_id:
                        row['Date Removed'] = current_date  # Set the removal date
                        removed = True
                    rows.append(row)

            if removed:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        'Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'
                    ])
                    writer.writeheader()
                    writer.writerows(rows)

            return removed

        except FileNotFoundError:
            print("Inventory file not found.")
            return False

    
    def auto_order(self):
        reorder_made = False
        rows = []
        current_date = datetime.now().strftime('%Y-%m-%d')
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['Quantity']) < self.auto_reorder_threshold:
                        row['Quantity'] = str(int(row['Quantity']) + self.low_stock_threshold)
                        row['Date Updated'] = current_date
                        reorder_made = True
                    rows.append(row)

            with open(self.inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'Item', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed'
                ])
                writer.writeheader()
                writer.writerows(rows)
        except FileNotFoundError:
            print("Inventory file not found.")
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

    def check_exp_date(self):
        expiring_items = []
        today = datetime.today()
        threshold_date = today + timedelta(days=30)
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    exp_date = row.get('Expiration Date', '')
                    if exp_date and datetime.strptime(exp_date, "%Y-%m-%d") <= threshold_date:
                        expiring_items.append((row['Item'], row['ID'], row['Quantity'], exp_date))
        except FileNotFoundError:
            print("Inventory file not found.")
        return expiring_items



# #Inventory.py
# import csv
# import os
# from src.LoginRoles import LoginRoles  # Import the LoginRoles class

# class Inventory:
#     def __init__(self, low_stock_threshold=10, auto_reorder_threshold=5, inventory_file='DBFiles/db_inventory.csv', filled_file='DBFiles/db_filled_prescription.csv', picked_up_file='DBFiles/db_picked_up_prescription.csv'):
#         # Set up the base directory path
#         base_path = os.path.dirname(os.path.abspath(__file__))

#         # Ensure the 'DBFiles' directory exists, if not, create it
#         db_dir = os.path.join(base_path, 'DBFiles')
#         if not os.path.exists(db_dir):
#             os.makedirs(db_dir)

#         # Set the file paths relative to the base directory
#         self.inventory_file = os.path.join(base_path, inventory_file)
#         self.filled_file = os.path.join(base_path, filled_file)
#         self.picked_up_file = os.path.join(base_path, picked_up_file)

#         # Ensure the inventory file exists, and create it if necessary
#         self.ensure_inventory_file_exists()

#         self.low_stock_threshold = low_stock_threshold
#         self.auto_reorder_threshold = auto_reorder_threshold
#         self.login_roles = LoginRoles()  # Create an instance of the LoginRoles class

#     def ensure_inventory_file_exists(self):
#         """
#         Ensure that the inventory file exists. If not, create the file with a header row.
#         """
#         if not os.path.isfile(self.inventory_file):
#             with open(self.inventory_file, mode='w', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['Medication', 'ID', 'Quantity'])  # Write the header
# def view_stock(self):
#     try:
#         with open(self.inventory_file, mode='r') as file:
#             reader = csv.reader(file)
#             next(reader)  # Skip header
#             stock_empty = True
#             print("Current inventory stock:")
#             for medication, item_id, quantity in reader:
#                 stock_empty = False
#                 print(f"{medication} (ID: {item_id}): {quantity} units")
#             if stock_empty:
#                 print("The inventory is currently empty.")
#     except FileNotFoundError:
#         print("Inventory file not found. The inventory is currently empty.")


#     def update_stock(self, medication, new_id, new_quantity):
#         """
#         Updates the stock for a specific medication in the CSV, allowing changes to Medication, ID, and Quantity.
#         If the medication with the given ID exists, it is updated. Otherwise, it adds a new entry.
#         """
#         updated = False
#         rows = []

#         try:
#             # Read the current inventory file
#             with open(self.inventory_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 header = next(reader)  # Skip the header

#                 for row in reader:
#                     # Check if the row matches the medication name and ID
#                     if len(row) == 3 and row[0].strip().lower() == medication.strip().lower() and row[1].strip() == new_id.strip():
#                         # Update the quantity of the existing entry
#                         row[2] = str(new_quantity)
#                         updated = True
#                         print(f"Updated {medication} with ID {new_id}: new quantity is {new_quantity}")
#                     rows.append(row)

#             if not updated:
#                 print(f"Item {medication} (ID: {new_id}) not found, adding as a new item.")
#                 rows.append([medication, new_id, str(new_quantity)])

#         except FileNotFoundError:
#             print("Inventory file not found. Creating a new inventory.")
#             rows.append([medication, new_id, str(new_quantity)])

#         # Write the updated inventory back to the file
#         with open(self.inventory_file, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Medication', 'ID', 'Quantity'])  # Write the header
#             writer.writerows(rows)

#         print(f"Inventory updated for {medication} (ID: {new_id}): {new_quantity} units.")

#     def update_stock(self, medication, new_id, new_quantity):
#         """
#         Updates the stock for a specific medication in the CSV, allowing changes to Medication, ID, and Quantity.
#         If the medication with the given ID exists, it is updated. Otherwise, it adds a new entry.
#         """
#         updated = False
#         rows = []

#         try:
#             # Read the current inventory file
#             with open(self.inventory_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 header = next(reader)  # Skip the header

#                 for row in reader:
#                     # Check if the row matches the medication name and ID
#                     if len(row) == 3 and row[0].strip().lower() == medication.strip().lower() and row[1].strip() == new_id.strip():
#                         # Update the quantity of the existing entry
#                         row[2] = str(new_quantity)
#                         updated = True
#                         print(f"Updated {medication} with ID {new_id}: new quantity is {new_quantity}")
#                     rows.append(row)

#         except FileNotFoundError:
#             print("Inventory file not found. Creating a new inventory.")

#         # If the medication was found, update the quantity; if not, add a new entry
#         if not updated:
#             rows.append([medication, new_id, str(new_quantity)])
#             print(f"Added new entry: {medication} with ID {new_id}: {new_quantity} units")

#         # Write the updated inventory back to the file
#         with open(self.inventory_file, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Medication', 'ID', 'Quantity'])  # Write the header
#             writer.writerows(rows)

#         print(f"Inventory updated for {medication} (ID: {new_id}): {new_quantity} units.")



#     def auto_order(self):
#         rows = []
#         updated = False
        
#         try:
#             with open(self.inventory_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 header = next(reader)  # Skip header
#                 for row in reader:
#                     medication, quantity = row
#                     quantity = int(quantity)
#                     if quantity < self.auto_reorder_threshold:
#                         order_quantity = quantity + (self.low_stock_threshold * 2)
#                         quantity += order_quantity
#                         print(f"Automatic reorder placed for {medication}. {order_quantity} units added to stock.")
#                         updated = True
#                     rows.append([medication, str(quantity)])

#             if updated:
#                 with open(self.inventory_file, mode='w', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(header)
#                     writer.writerows(rows)

#         except FileNotFoundError:
#             print("Inventory file not found. No auto-order can be placed.")

#     def order_medication(self, medication, quantity, username, password):
#         # Restricts ordering medications to managers only
#         login_success, message = self.login_roles.login(username, password)
        
#         if login_success:
#             role = self.login_roles.find_user_role(username)
#             if role == "manager":
#                 print(f"{username} (Manager) is ordering {quantity} units of {medication}.")
#                 self.update_stock(medication, quantity)
#             else:
#                 print(f"Permission denied. Only managers can order medications.")
#         else:
#             print(f"Login failed: {message}")

#     def remove_medication(self, medication):
#         rows = []
#         found = False
#         try:
#             with open(self.inventory_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip header
#                 for row in reader:
#                     if row[0] != medication:
#                         rows.append(row)
#                     else:
#                         found = True

#             if found:
#                 with open(self.inventory_file, mode='w', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(['Medication', 'Quantity'])
#                     writer.writerows(rows)
#                 print(f"{medication} has been removed from the inventory.")
#             else:
#                 print(f"{medication} is not in the inventory.")
#         except FileNotFoundError:
#             print("Inventory file not found. Nothing to remove.")

#     def check_low_stock(self):
#         low_stock_items = []
#         try:
#             with open(self.inventory_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip header
#                 for medication, quantity in reader:
#                     if int(quantity) < self.low_stock_threshold:
#                         low_stock_items.append((medication, quantity))

#             if low_stock_items:
#                 print("Low stock alert for the following medications:")
#                 for item in low_stock_items:
#                     print(f"{item[0]}: Only {item[1]} units left!")
#             else:
#                 print("No low stock medications at the moment.")
#         except FileNotFoundError:
#             print("Inventory file not found. No low stock medications to report.")

#     def fill_prescription(self, medication, quantity):
#         rows = []
#         try:
#             with open(self.inventory_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 header = next(reader)
#                 medication_found = False
#                 for row in reader:
#                     if row[0] == medication:
#                         if int(row[1]) >= quantity:
#                             row[1] = str(int(row[1]) - quantity)
#                             medication_found = True
#                         else:
#                             print(f"Insufficient stock for {medication}.")
#                             return
#                     rows.append(row)

#             if medication_found:
#                 with open(self.inventory_file, mode='w', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(header)
#                     writer.writerows(rows)
#                 print(f"{quantity} units of {medication} dispensed.")
#                 self.add_filled_prescription(medication, quantity)
#                 self.check_low_stock()
#             else:
#                 print(f"{medication} is not in the inventory.")

#         except FileNotFoundError:
#             print("Inventory file not found.")

#     def add_filled_prescription(self, medication, quantity):
#         with open(self.filled_file, mode='a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([medication, quantity])

#     def pick_up_prescription(self, medication, quantity):
#         # Check if the prescription exists in the filled prescriptions file
#         found = False
#         try:
#             with open(self.filled_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip header
#                 for row in reader:
#                     if row[0] == medication and int(row[1]) == quantity:
#                         found = True
#                         break

#             if found:
#                 # Log the picked-up prescription without modifying the filled file
#                 self.add_picked_up_prescription(medication, quantity)
#                 print(f"{quantity} units of {medication} picked up.")
#             else:
#                 print("Prescription not found in filled prescriptions.")
#         except FileNotFoundError:
#             print("Filled prescriptions file not found.")

#     def add_picked_up_prescription(self, medication, quantity):
#         with open(self.picked_up_file, mode='a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([medication, quantity])

#     def view_filled_prescriptions(self):
#         try:
#             with open(self.filled_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip header
#                 print("Filled prescriptions:")
#                 for row in reader:
#                     print(f"{row[1]} units of {row[0]}")
#         except FileNotFoundError:
#             print("No filled prescriptions at the moment.")

#     def view_picked_up_prescriptions(self):
#         try:
#             with open(self.picked_up_file, mode='r') as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip header
#                 print("Picked up prescriptions:")
#                 for row in reader:
#                     print(f"{row[1]} units of {row[0]}")
#         except FileNotFoundError:
#             print("No picked-up prescriptions at the moment.")
    
#     def clear_picked_up_prescriptions(self): #FIXME: not sure if we want to have this method or not? If we continuously store the picked up prescriptions, the file might get large
#         try:
#             with open(self.picked_up_file, mode='w', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['Medication', 'Quantity'])  # Write only the header
#             print("Picked-up prescriptions have been cleared.")
#         except FileNotFoundError:
#             print("Picked-up prescriptions file not found.")