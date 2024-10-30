#InventoryUI.py
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import csv
from Inventory import Inventory

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

        # Set a minimum size for the dashboard
        self.setMinimumSize(1100, 600) # Example size, you can adjust these values

        # Initialize the inventory table
        self.initialize_table()

        # Connect cellChanged signal to check for last row usage
        self.ItemsTable.cellChanged.connect(self.add_row_if_last_row_used)

    def initialize_table(self):
        """
        Set up the inventory table to display data.
        """
        self.ItemsTable.setColumnCount(4)  # Columns for Medication, ID, Quantity
        self.ItemsTable.setHorizontalHeaderLabels(['Medication', 'ID', 'Quantity', 'Expiration Date'])
        self.load_inventory_into_table()

    def load_inventory_into_table(self):
        """
        Load inventory data from the CSV file into the QTableWidget.
        """
        self.ItemsTable.setRowCount(0)  # Clear the table
        inventory_data = self.inventory.read_inventory_data()  # Read from inventory CSV
        for i, item in enumerate(inventory_data):
            self.ItemsTable.insertRow(i)
            self.ItemsTable.setItem(i, 0, QTableWidgetItem(item['Medication']))
            self.ItemsTable.setItem(i, 1, QTableWidgetItem(item['ID']))
            self.ItemsTable.setItem(i, 2, QTableWidgetItem(item['Quantity']))
            self.ItemsTable.setItem(i, 3, QTableWidgetItem(item['Expiration Date']))

        # Add an empty row at the end
        self.add_empty_row()

      

    def add_empty_row(self):
        """
        Adds an empty row to the end of the ItemsTable.
        """
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)
        self.ItemsTable.setItem(row_count, 0, QTableWidgetItem(""))  # Medication
        self.ItemsTable.setItem(row_count, 1, QTableWidgetItem(""))  # ID
        self.ItemsTable.setItem(row_count, 2, QTableWidgetItem(""))  # Quantity
        self.ItemsTable.setItem(row_count, 3, QTableWidgetItem(""))  # Expiration Date

    def add_row_if_last_row_used(self, row, column):
        """
        Adds a new empty row if the last row in the table is used.
        """
        row_count = self.ItemsTable.rowCount()
        # Check if the current cell being edited is in the last row and contains data
        if row == row_count - 1 and any(self.ItemsTable.item(row, col) for col in range(self.ItemsTable.columnCount())):
            # Temporarily block the cellChanged signal to avoid recursion
            self.ItemsTable.blockSignals(True)
            self.add_empty_row()
            self.ItemsTable.blockSignals(False)


    def update_inventory(self):
        """
        Update stock for a specific medication from the selected row in the table.
        """
        selected_row = self.ItemsTable.currentRow()
        if selected_row != -1:
            medication = self.ItemsTable.item(selected_row, 0).text()
            id = self.ItemsTable.item(selected_row, 1).text()  # ID from the second column
            new_quantity_str = self.ItemsTable.item(selected_row, 2).text()
            expiration_date = self.ItemsTable.item(selected_row, 3).text()

            try:
                new_quantity = int(new_quantity_str)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid quantity entered.")
                return

            self.inventory.update_stock(medication, id, new_quantity, expiration_date)
            QMessageBox.information(self, "Success", f"Updated {medication} (ID: {id}) stock to {new_quantity}, Expiration Date: {expiration_date}")
        else:
            QMessageBox.warning(self, "Error", "Please select a row to update!")

    def auto_order_stock(self):
        """Trigger auto reorder in inventory and reload table."""
        reorder_made = self.inventory.auto_order()
        self.load_inventory_into_table()  # Refresh table after attempting reorder
        if reorder_made:
            QMessageBox.information(self, "Auto Order", "Auto reorder placed for low-stock items.")
        else:
            QMessageBox.information(self, "Auto Order", "No items required reordering.")


    def check_low_stock(self):
        low_stock_items = self.inventory.check_low_stock()
    
        if low_stock_items:
            message = "Low stock alert for the following medications:\n"
            for item in low_stock_items:
                medication, item_id, quantity, exp_date = item
                message += f"- {medication} (ID: {item_id}): {quantity} units left, Expiration Date: {exp_date}\n"
            
            QMessageBox.warning(self, "Low Stock Alert", message)
        else:
            QMessageBox.information(self, "Low Stock Alert", "No low stock medications at the moment.")

    def cancel(self):
        from src.Dashboard import Dashboard  # Move the import here to avoid circular import


        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)

        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)
