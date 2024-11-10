#InventoryUI.py
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import csv
from Inventory import Inventory
from LoginRoles import LoginRoles


class InventoryUI(QMainWindow):
    def __init__(self, widget, username):
        super(InventoryUI, self).__init__()
        self.widget = widget
        self.inventory = Inventory()
        self.username = username

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
        """
        Set up the inventory table to display data.
        """
        self.ItemsTable.setColumnCount(5)
        self.ItemsTable.setHorizontalHeaderLabels(['Item', 'ID', 'Quantity', 'Price', 'Expiration Date'])
        self.load_inventory_into_table()

    def load_inventory_into_table(self):
        """
        Load inventory data from the CSV file into the QTableWidget.
        """
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
        """
        Remove the selected item from the table and CSV file.
        """
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
            # Remove from CSV
            success = self.inventory.remove_item(item, item_id)
            if success:
                # Remove row from table
                self.ItemsTable.removeRow(selected_row)
                QMessageBox.information(self, "Success", f"Item '{item}' (ID: {item_id}) has been removed.")
            else:
                QMessageBox.warning(self, "Error", "Failed to remove the item from the inventory.")

    def add_empty_row(self):
        """
        Add an empty row to the inventory table.
        """
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)
        self.ItemsTable.setItem(row_count, 0, QTableWidgetItem(""))  # Item
        self.ItemsTable.setItem(row_count, 1, QTableWidgetItem(""))  # ID
        self.ItemsTable.setItem(row_count, 2, QTableWidgetItem(""))  # Quantity
        self.ItemsTable.setItem(row_count, 3, QTableWidgetItem(""))  # Price
        self.ItemsTable.setItem(row_count, 4, QTableWidgetItem(""))  # Expiration Date
        
    def update_inventory(self):
        """
        Update stock for a specific item from the selected row in the table.
        """
        selected_row = self.ItemsTable.currentRow()
        if selected_row != -1:
            item = self.ItemsTable.item(selected_row, 0).text()
            item_id = self.ItemsTable.item(selected_row, 1).text()  # ID from the second column
            new_quantity_str = self.ItemsTable.item(selected_row, 2).text()
            price = self.ItemsTable.item(selected_row, 3).text()  # Price column
            expiration_date = self.ItemsTable.item(selected_row, 4).text()

            try:
                new_quantity = int(new_quantity_str)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid quantity entered.")
                return

            self.inventory.update_stock(item, item_id, new_quantity, expiration_date, price)
            QMessageBox.information(
                self, "Success",
                f"Updated {item} (ID: {item_id}) stock to {new_quantity}, Price: {price}, Expiration Date: {expiration_date}"
            )
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
        from src.Dashboard import Dashboard  # Move the import here to avoid circular import

        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)

    def check_exp_date(self):
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
