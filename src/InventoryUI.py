#InventoryUI.py
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
from Inventory import Inventory
from datetime import datetime

class InventoryUI(QMainWindow):
    def __init__(self, widget, username): #Takes in the widget and current username as parameters
        super(InventoryUI, self).__init__()
        self.widget = widget
        self.username = username
        
        # Initialize the Inventory class
        self.inventory = Inventory()

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Inventory.ui')
        if not os.path.exists(ui_path):
            print(f"UI file not found at: {ui_path}")
        loadUi(ui_path, self)

        # Connect buttons
        self.cancelButton.clicked.connect(self.cancel)
        self.viewStockButton.clicked.connect(self.load_inventory_into_table)
        self.updateStockButton.clicked.connect(self.update_inventory)
        self.autoOrderButton.clicked.connect(self.auto_order_stock)
        self.lowStockButton.clicked.connect(self.check_low_stock)
        self.exp_date.clicked.connect(self.check_exp_date)
        self.inv_row.clicked.connect(self.add_empty_row)
        self.removeItem.clicked.connect(self.remove_selected_item)  # Connect remove button

        # Set a minimum size for the dashboard
        self.setMinimumSize(1100, 600)

        # Initialize the inventory table
        self.initialize_table()


    def initialize_table(self):
        # Populates the table with the inventory data on load
        self.ItemsTable.setColumnCount(5)
        self.ItemsTable.setHorizontalHeaderLabels(['Item', 'ID', 'Quantity', 'Price', 'Expiration Date'])
        self.load_inventory_into_table()


    def load_inventory_into_table(self):
        # Loads the actual inventory data into the table
        self.ItemsTable.setRowCount(0)  # Clear the table
        inventory_data = self.inventory.read_inventory_data()  # Read from inventory CSV
        for i, item in enumerate(inventory_data):
            self.ItemsTable.insertRow(i)
            self.ItemsTable.setItem(i, 0, QTableWidgetItem(item['Item']))
            self.ItemsTable.setItem(i, 1, QTableWidgetItem(item['ID']))
            self.ItemsTable.setItem(i, 2, QTableWidgetItem(item['Quantity']))
            self.ItemsTable.setItem(i, 3, QTableWidgetItem(item['Price']))
            self.ItemsTable.setItem(i, 4, QTableWidgetItem(item['Expiration Date']))


    def remove_selected_item(self):
        selected_row = self.ItemsTable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a row to remove!")
            return

        # Retrieve item details
        item = self.ItemsTable.item(selected_row, 0).text()  # Item name
        item_id = self.ItemsTable.item(selected_row, 1).text()  # Item ID

        # Confirm deletion
        confirmation = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove the item '{item}' (ID: {item_id})?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            # Update CSV using `remove_medication`
            success = self.inventory.remove_medication(item_id)
            if success:
                # Remove row from GUI table
                self.ItemsTable.removeRow(selected_row)
                QMessageBox.information(self, "Success", f"Item '{item}' (ID: {item_id}) has been marked as removed.")
            else:
                QMessageBox.warning(self, "Error", "Failed to remove the item from the inventory.")



    def add_empty_row(self):
        # Adds an empty row to the table
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)
        self.ItemsTable.setItem(row_count, 0, QTableWidgetItem(""))  # Item
        self.ItemsTable.setItem(row_count, 1, QTableWidgetItem(""))  # ID
        self.ItemsTable.setItem(row_count, 2, QTableWidgetItem(""))  # Quantity
        self.ItemsTable.setItem(row_count, 3, QTableWidgetItem(""))  # Price
        self.ItemsTable.setItem(row_count, 4, QTableWidgetItem(""))  # Expiration Date
        
        
    def update_inventory(self):
        selected_row = self.ItemsTable.currentRow()
        if selected_row != -1:
            try:
                item = self.ItemsTable.item(selected_row, 0).text().strip()
                item_id = self.ItemsTable.item(selected_row, 1).text().strip()
                new_quantity_str = self.ItemsTable.item(selected_row, 2).text().strip()
                price = self.ItemsTable.item(selected_row, 3).text().strip()
                expiration_date = self.ItemsTable.item(selected_row, 4).text().strip()

                # Validate Quantity
                try:
                    new_quantity = int(new_quantity_str)
                    if new_quantity < 0:
                        raise ValueError("Quantity cannot be negative.")
                except ValueError:
                    QMessageBox.warning(self, "Error", f"Invalid quantity: {new_quantity_str}.")
                    return

                # Validate Price
                try:
                    float(price)  # Convert to float to validate
                except ValueError:
                    QMessageBox.warning(self, "Error", f"Invalid price: {price}.")
                    return

                # Validate Expiration Date
                try:
                    datetime.strptime(expiration_date, '%Y-%m-%d')
                except ValueError:
                    QMessageBox.warning(self, "Error", f"Invalid expiration date: {expiration_date}. Use YYYY-MM-DD.")
                    return

                # Update inventory
                self.inventory.update_stock(item, item_id, new_quantity, price, expiration_date)
                QMessageBox.information(self, "Success", f"Item '{item}' updated successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please select a row to update!")



    def auto_order_stock(self):
        # Run auto_order to check if reorder is needed and refresh inventory table
        reorder_made = self.inventory.auto_order()

        if reorder_made:
            QMessageBox.information(self, "Auto Order", "Auto reorder placed for low-stock items.")
        else:
            QMessageBox.information(self, "Auto Order", "No items required reordering.")

        self.load_inventory_into_table()  # Refresh table after attempting reorder


    def check_low_stock(self):
        # Check for low stock items and display a message
        low_stock_items = self.inventory.check_low_stock()

        if low_stock_items:
            message = "Low stock alert for the following items:\n"
            for item in low_stock_items:
                item_name, item_id, quantity = item
                message += f"- {item_name} (ID: {item_id}): {quantity} units left\n"

            QMessageBox.warning(self, "Low Stock Alert", message)
        else:
            QMessageBox.information(self, "Low Stock Alert", "No low stock items at the moment.")


    def cancel(self):
        # Return to the dashboard
        from src.Dashboard import Dashboard  # Move the import here to avoid circular import

        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)


    def check_exp_date(self):
        # Check for items close to expiration date and display a message
        exp_date_items = self.inventory.check_exp_date()

        if exp_date_items:
            message = "Expiration date alert for the following items:\n"
            for item in exp_date_items:
                item_name, item_id, quantity, exp_date = item
                message += f"- {item_name} (ID: {item_id}): {quantity} units left, Expiration Date: {exp_date}\n"

            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Expiration Date Alert")
            msg_box.setText(message)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("QLabel{min-width: 400px;}")
            msg_box.exec_()
        else:
            QMessageBox.information(self, "Expiration Date Alert", "No items are close to expiration date.")
