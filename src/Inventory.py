import csv
import os
from datetime import datetime, timedelta
from LoginRoles import LoginRoles  # Assuming this class handles login-related roles


class Inventory:
    def __init__(self, low_stock_threshold=120, auto_reorder_threshold=120,
                 inventory_file='../DBFiles/db_inventory.csv',
                 activity_file='../DBFiles/db_inventory_activity_log.csv',
                 filled_file='../DBFiles/db_filled_prescription.csv',
                 picked_up_file='../DBFiles/db_picked_up_prescription.csv'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        print(f"Base path: {base_path}")

        self.inventory_file = os.path.join(base_path, inventory_file)
        self.activity_file = os.path.join(base_path, activity_file)
        self.filled_file = os.path.join(base_path, filled_file)
        self.picked_up_file = os.path.join(base_path, picked_up_file)

        # Ensure inventory file structure
        self.initialize_csv(self.inventory_file, ['Medication', 'ID', 'Quantity', 'Price', 'Expiration Date'])
        self.initialize_csv(self.activity_file, ['Medication', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Action', 'Date'])
        self.initialize_csv(self.filled_file, ['Medication', 'Quantity'])
        self.initialize_csv(self.picked_up_file, ['Medication', 'Quantity'])

        self.low_stock_threshold = low_stock_threshold
        self.auto_reorder_threshold = auto_reorder_threshold

    def initialize_csv(self, file_path, headers):
        """Initialize a CSV file with headers if it doesn't exist."""
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

    def read_inventory_data(self):
        """Read inventory data and return it as a list of dictionaries."""
        inventory_data = []
        try:
            with open(self.inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    inventory_data.append(row)
        except FileNotFoundError:
            print("Inventory file not found.")
        return inventory_data

    def update_stock(self, medication, item_id, quantity, price, expiration_date):
        """Update or add stock for a medication."""
        inventory_data = self.read_inventory_data()
        updated = False

        for item in inventory_data:
            if item['ID'] == item_id:
                item['Quantity'] = str(quantity)
                item['Price'] = str(price)
                item['Expiration Date'] = expiration_date
                updated = True

        if not updated:
            inventory_data.append({
                'Medication': medication,
                'ID': item_id,
                'Quantity': str(quantity),
                'Price': str(price),
                'Expiration Date': expiration_date
            })

        self.write_inventory_data(inventory_data)
        print(f"Stock updated for {medication} (ID: {item_id}).")

    def write_inventory_data(self, data):
        """Write updated inventory data to the CSV file."""
        with open(self.inventory_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Medication', 'ID', 'Quantity', 'Price', 'Expiration Date'])
            writer.writeheader()
            writer.writerows(data)

    def check_low_stock(self):
        """Check for medications below the stock threshold."""
        low_stock_items = []
        inventory_data = self.read_inventory_data()

        for item in inventory_data:
            if int(item['Quantity']) < self.low_stock_threshold:
                low_stock_items.append(item)
        return low_stock_items

    def auto_order(self):
        """Automatically reorder low-stock items."""
        inventory_data = self.read_inventory_data()
        reorder_made = False

        for item in inventory_data:
            if int(item['Quantity']) < self.auto_reorder_threshold:
                item['Quantity'] = str(int(item['Quantity']) + self.low_stock_threshold)
                reorder_made = True

        if reorder_made:
            self.write_inventory_data(inventory_data)
            print("Auto reorder completed.")
        else:
            print("No items needed auto reorder.")

    def check_exp_date(self):
        """Check for medications nearing expiration."""
        expiring_items = []
        inventory_data = self.read_inventory_data()
        today = datetime.today()
        threshold = today + timedelta(days=30)

        for item in inventory_data:
            exp_date = datetime.strptime(item['Expiration Date'], "%Y-%m-%d")
            if exp_date <= threshold:
                expiring_items.append(item)
        return expiring_items

    def remove_medication(self, item_id):
        """Remove a medication by ID."""
        inventory_data = self.read_inventory_data()
        updated_data = [item for item in inventory_data if item['ID'] != item_id]

        if len(updated_data) != len(inventory_data):
            self.write_inventory_data(updated_data)
            print(f"Medication with ID {item_id} removed.")
        else:
            print(f"Medication with ID {item_id} not found.")

    def log_action(self, medication, item_id, action):
        """Log an inventory action in the activity log."""
        with open(self.activity_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([medication, item_id, action, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print(f"Action logged: {action} for {medication} (ID: {item_id}).")
