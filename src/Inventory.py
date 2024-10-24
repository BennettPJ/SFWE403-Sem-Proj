import csv
import os
from src.LoginRoles import LoginRoles  # Import the LoginRoles class

class Inventory:
    def __init__(self, low_stock_threshold=10, auto_reorder_threshold=5, inventory_file='DBFiles/db_inventory.csv', filled_file='DBFiles/db_filled_prescription.csv', picked_up_file='DBFiles/db_picked_up_prescription.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.inventory_file = os.path.join(base_path, inventory_file)
        self.filled_file = os.path.join(base_path, filled_file)
        self.picked_up_file = os.path.join(base_path, picked_up_file)
        self.low_stock_threshold = low_stock_threshold
        self.auto_reorder_threshold = auto_reorder_threshold
        self.login_roles = LoginRoles()  # Create an instance of the LoginRoles class

    def view_stock(self):
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                stock_empty = True
                print("Current inventory stock:")
                for medication, quantity in reader:
                    stock_empty = False
                    print(f"{medication}: {quantity} units")
                if stock_empty:
                    print("The inventory is currently empty.")
        except FileNotFoundError:
            print("Inventory file not found. The inventory is currently empty.")

    def update_stock(self, medication, quantity):
        updated = False
        rows = []

        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row[0] == medication:
                        row[1] = str(int(row[1]) + quantity)  # Update quantity IMPORTANT maybe FIXME: currently I have behavior that sets quantity to current quantity + new quantity input.
                        updated = True
                    rows.append(row)

            if not updated:  # If medication is not found, add it
                rows.append([medication, str(quantity)])

        except FileNotFoundError:
            rows.append([medication, str(quantity)])  # Add the medication if the file doesn't exist

        with open(self.inventory_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Medication', 'Quantity'])
            writer.writerows(rows)
        print(f"Updated stock for {medication}: {quantity} units added.")

    def auto_order(self):
        rows = []
        updated = False
        
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                for row in reader:
                    medication, quantity = row
                    quantity = int(quantity)
                    if quantity < self.auto_reorder_threshold:
                        order_quantity = quantity + (self.low_stock_threshold * 2)
                        quantity += order_quantity
                        print(f"Automatic reorder placed for {medication}. {order_quantity} units added to stock.")
                        updated = True
                    rows.append([medication, str(quantity)])

            if updated:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(rows)

        except FileNotFoundError:
            print("Inventory file not found. No auto-order can be placed.")

    def order_medication(self, medication, quantity, username, password):
        # Restricts ordering medications to managers only
        login_success, message = self.login_roles.login(username, password)
        
        if login_success:
            role = self.login_roles.find_user_role(username)
            if role == "manager":
                print(f"{username} (Manager) is ordering {quantity} units of {medication}.")
                self.update_stock(medication, quantity)
            else:
                print(f"Permission denied. Only managers can order medications.")
        else:
            print(f"Login failed: {message}")

    def remove_medication(self, medication):
        rows = []
        found = False
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row[0] != medication:
                        rows.append(row)
                    else:
                        found = True

            if found:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Medication', 'Quantity'])
                    writer.writerows(rows)
                print(f"{medication} has been removed from the inventory.")
            else:
                print(f"{medication} is not in the inventory.")
        except FileNotFoundError:
            print("Inventory file not found. Nothing to remove.")

    def check_low_stock(self):
        low_stock_items = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for medication, quantity in reader:
                    if int(quantity) < self.low_stock_threshold:
                        low_stock_items.append((medication, quantity))

            if low_stock_items:
                print("Low stock alert for the following medications:")
                for item in low_stock_items:
                    print(f"{item[0]}: Only {item[1]} units left!")
            else:
                print("No low stock medications at the moment.")
        except FileNotFoundError:
            print("Inventory file not found. No low stock medications to report.")

    def fill_prescription(self, medication, quantity):
        rows = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                medication_found = False
                for row in reader:
                    if row[0] == medication:
                        if int(row[1]) >= quantity:
                            row[1] = str(int(row[1]) - quantity)
                            medication_found = True
                        else:
                            print(f"Insufficient stock for {medication}.")
                            return
                    rows.append(row)

            if medication_found:
                with open(self.inventory_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(rows)
                print(f"{quantity} units of {medication} dispensed.")
                self.add_filled_prescription(medication, quantity)
                self.check_low_stock()
            else:
                print(f"{medication} is not in the inventory.")

        except FileNotFoundError:
            print("Inventory file not found.")

    def add_filled_prescription(self, medication, quantity):
        with open(self.filled_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([medication, quantity])

    def pick_up_prescription(self, medication, quantity):
        # Check if the prescription exists in the filled prescriptions file
        found = False
        try:
            with open(self.filled_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row[0] == medication and int(row[1]) == quantity:
                        found = True
                        break

            if found:
                # Log the picked-up prescription without modifying the filled file
                self.add_picked_up_prescription(medication, quantity)
                print(f"{quantity} units of {medication} picked up.")
            else:
                print("Prescription not found in filled prescriptions.")
        except FileNotFoundError:
            print("Filled prescriptions file not found.")

    def add_picked_up_prescription(self, medication, quantity):
        with open(self.picked_up_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([medication, quantity])

    def view_filled_prescriptions(self):
        try:
            with open(self.filled_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                print("Filled prescriptions:")
                for row in reader:
                    print(f"{row[1]} units of {row[0]}")
        except FileNotFoundError:
            print("No filled prescriptions at the moment.")

    def view_picked_up_prescriptions(self):
        try:
            with open(self.picked_up_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                print("Picked up prescriptions:")
                for row in reader:
                    print(f"{row[1]} units of {row[0]}")
        except FileNotFoundError:
            print("No picked-up prescriptions at the moment.")
    
    def clear_picked_up_prescriptions(self): #FIXME: not sure if we want to have this method or not? If we continuously store the picked up prescriptions, the file might get large
        try:
            with open(self.picked_up_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Medication', 'Quantity'])  # Write only the header
            print("Picked-up prescriptions have been cleared.")
        except FileNotFoundError:
            print("Picked-up prescriptions file not found.")