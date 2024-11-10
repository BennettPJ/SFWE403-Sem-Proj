from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import csv
from Inventory import Inventory
from LoginRoles import LoginRoles


class InventoryUI(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
        super(InventoryUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.inventory = Inventory()  # Create an instance of the Inventory class
        self.username = username  # Store the username

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Inventory.ui')
        if not os.path.exists(ui_path):
            print(f"UI file not found at: {ui_path}")  # Debug print
        loadUi(ui_path, self)

        # Connect buttons
        self.cancelButton.clicked.connect(self.cancel)  # Cancel button
        self.viewStockButton.clicked.connect(self.load_inventory_into_table)  # View stock button
        self.updateStockButton.clicked.connect(self.update_inventory)  # Update inventory button
        self.autoOrderButton.clicked.connect(self.auto_order_stock)  # Auto reorder button
        self.lowStockButton.clicked.connect(self.check_low_stock)  # Check low stock button
        self.exp_date.clicked.connect(self.check_exp_date)  # Expiration date button
        self.inv_row.clicked.connect(self.add_empty_row)  # Add row button
        self.removeItem.clicked.connect(self.remove_item)  # Remove item button

        # Set a minimum size for the dashboard
        self.setMinimumSize(1100, 600)  # Example size, you can adjust these values

        # Initialize the inventory table
        self.initialize_table()

        # Set up UI based on user roles
        self.setup_ui()

    def setup_ui(self):
        """Enable or disable UI features based on user roles."""
        self.autoOrderButton.setEnabled(True)  # Enable by default
        roles = LoginRoles()
        user_role = roles.find_user_role(self.username)
        if user_role != 'manager':
            self.autoOrderButton.setEnabled(False)

    def initialize_table(self):
        """Set up the inventory table to display data."""
        self.ItemsTable.setColumnCount(5)  # Adjusted to include Price
        self.ItemsTable.setHorizontalHeaderLabels(['Medication', 'ID', 'Quantity', 'Price', 'Expiration Date'])
        self.load_inventory_into_table()

    def load_inventory_into_table(self):
        """Load inventory data from the CSV file into the QTableWidget."""
        self.ItemsTable.setRowCount(0)  # Clear the table
        try:
            inventory_data = self.inventory.read_inventory_data()  # Read from inventory CSV

            for i, item in enumerate(inventory_data):
                self.ItemsTable.insertRow(i)
                self.ItemsTable.setItem(i, 0, QTableWidgetItem(item['Medication']))
                self.ItemsTable.setItem(i, 1, QTableWidgetItem(item['ID']))
                self.ItemsTable.setItem(i, 2, QTableWidgetItem(item['Quantity']))
                self.ItemsTable.setItem(i, 3, QTableWidgetItem(item['Price']))
                self.ItemsTable.setItem(i, 4, QTableWidgetItem(item['Expiration Date']))

            # Add an empty row at the end
            self.add_empty_row()

        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Missing column in inventory: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load inventory: {str(e)}")
    def check_exp_date(self):
        """Check for medications nearing expiration and notify the user."""
        expiring_items = self.inventory.check_exp_date()

        if expiring_items:
            message = "Expiration date alert for the following medications:\n"
            for item in expiring_items:
                message += f"- {item['Medication']} (ID: {item['ID']}): {item['Quantity']} units, Expiration Date: {item['Expiration Date']}\n"
            QMessageBox.warning(self, "Expiration Date Alert", message)
        else:
            QMessageBox.information(self, "Expiration Date Alert", "No medications nearing expiration.")

    def add_empty_row(self):
        """Add an empty row at the end of the table."""
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)
        for i in range(5):  # 5 columns
            self.ItemsTable.setItem(row_count, i, QTableWidgetItem(""))

    def update_inventory(self):
        """Update stock for a specific medication from the selected row in the table."""
        selected_row = self.ItemsTable.currentRow()
        if selected_row != -1:
            medication = self.ItemsTable.item(selected_row, 0).text()
            item_id = self.ItemsTable.item(selected_row, 1).text()
            new_quantity_str = self.ItemsTable.item(selected_row, 2).text()
            price = self.ItemsTable.item(selected_row, 3).text()
            expiration_date = self.ItemsTable.item(selected_row, 4).text()

            try:
                new_quantity = int(new_quantity_str)
                price = float(price)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid data entered.")
                return

            self.inventory.update_stock(medication, item_id, new_quantity, price, expiration_date)
            QMessageBox.information(self, "Success", f"Updated {medication} (ID: {item_id}).")
        else:
            QMessageBox.warning(self, "Error", "Please select a row to update!")

    def auto_order_stock(self):
        """Automatically reorder low-stock items."""
        reorder_made = self.inventory.auto_order()
        if reorder_made:
            QMessageBox.information(self, "Auto Order", "Auto reorder placed for low-stock items.")
        else:
            QMessageBox.information(self, "Auto Order", "No items required reordering.")
        self.load_inventory_into_table()

    def check_low_stock(self):
        """Identify medications that are low in stock."""
        low_stock_items = self.inventory.check_low_stock()
        if low_stock_items:
            message = "Low stock alert for the following medications:\n"
            for item in low_stock_items:
                message += f"{item['Medication']} (ID: {item['ID']}): {item['Quantity']} units left.\n"
            QMessageBox.warning(self, "Low Stock Alert", message)
        else:
            QMessageBox.information(self, "Low Stock Alert", "No low stock items.")

    def remove_item(self):
        """Remove a selected item from inventory."""
        selected_row = self.ItemsTable.currentRow()
        if selected_row != -1:
            item_id = self.ItemsTable.item(selected_row, 1).text()
            self.inventory.remove_item(item_id)
            self.ItemsTable.removeRow(selected_row)
            QMessageBox.information(self, "Success", f"Removed item ID {item_id}.")
        else:
            QMessageBox.warning(self, "Error", "Please select a row to remove!")

    def cancel(self):
        """Return to the dashboard."""
        from src.Dashboard import Dashboard
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)
