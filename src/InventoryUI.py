from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import csv
from Inventory import Inventory

class InventoryUI(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(InventoryUI, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        self.inventory = Inventory()  # Create an instance of the Inventory class

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Inventory.ui')
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
        self.ItemsTable.setColumnCount(3)  # Columns for Medication, ID, Quantity
        self.ItemsTable.setHorizontalHeaderLabels(['Medication', 'ID', 'Quantity'])
        self.load_inventory_into_table()

    def load_inventory_into_table(self):
        """
        Load inventory data from the CSV file into the QTableWidget.
        """
        self.ItemsTable.setRowCount(0)  # Clear the table
        try:
            with open(self.inventory.inventory_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for i, row in enumerate(reader):
                    self.ItemsTable.insertRow(i)

                    medication = row[0] if len(row) > 0 else "Unknown"
                    item_id = row[1] if len(row) > 1 else "Unknown"
                    quantity = row[2] if len(row) > 2 else "Missing Quantity"

                    self.ItemsTable.setItem(i, 0, QTableWidgetItem(medication))  # Medication
                    self.ItemsTable.setItem(i, 1, QTableWidgetItem(item_id))  # ID
                    self.ItemsTable.setItem(i, 2, QTableWidgetItem(quantity))  # Quantity

            # Add an empty row at the end
            self.add_empty_row()

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Inventory file not found!")
            # Add an empty row in case of file error
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

            try:
                new_quantity = int(new_quantity_str)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid quantity entered.")
                return

            self.inventory.update_stock(medication, id, new_quantity)
            QMessageBox.information(self, "Success", f"Updated {medication} (ID: {id}) stock to {new_quantity}")
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
        self.inventory.check_low_stock()

    def cancel(self):
        from src.Dashboard import Dashboard  # Move the import here to avoid circular import

        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)
