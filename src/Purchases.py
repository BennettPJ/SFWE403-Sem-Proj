from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.uic import loadUi
import os
import csv
from PyQt5.QtCore import pyqtSlot
from datetime import datetime  # Import datetime for recording the current date
from Inventory import Inventory


class Purchases(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
        super(Purchases, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.username = username  # Store the username
        self.inventory = Inventory() # instance of Inventory

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Purchase.ui')
        loadUi(ui_path, self)
        # Set a minimum size for the dashboard
        self.setMinimumSize(1100, 600)
        self.grandTotalLabel.setText("Grand Total: $0.00")

        self.addItemButton.clicked.connect(self.add_item)
        self.removeItemButton.clicked.connect(self.remove_item)
        self.cancelButton.clicked.connect(self.cancelPurchase)
        self.Complete.clicked.connect(self.complete_purchase)
        self.PrintReciept.clicked.connect(self.print_receipt)  # Connect the Print Receipt button

        # Connect changes in the ItemsTable to the function that recalculates the total.
        self.ItemsTable.itemChanged.connect(self.update_grand_total)

    def print_receipt(self):
        """Display a receipt of the current items in a new dialog window."""
        receipt_text = "Receipt\n"
        receipt_text += "-" * 40 + "\n"
        receipt_text += "{:<15} {:<10} {:<10} {:<10}\n".format("Item", "Qty", "Price", "Total")

        # Gather all items from the table.
        for row in range(self.ItemsTable.rowCount()):
            item = self.ItemsTable.item(row, 0).text() if self.ItemsTable.item(row, 0) else ""
            quantity = self.ItemsTable.item(row, 2).text() if self.ItemsTable.item(row, 2) else "0"
            price = self.ItemsTable.item(row, 3).text() if self.ItemsTable.item(row, 3) else "0.00"
            total = self.ItemsTable.item(row, 4).text() if self.ItemsTable.item(row, 4) else "0.00"

            # Format each row for the receipt.
            receipt_text += "{:<15} {:<10} {:<10} {:<10}\n".format(item, quantity, price, total)

        receipt_text += "-" * 40 + "\n"
        receipt_text += f"Payment Method: {self.PaymentMethod.currentText()}\n"
        receipt_text += f"{self.grandTotalLabel.text()}\n"
        receipt_text += "-" * 40 + "\n"

        # Create and show the receipt dialog.
        receipt_dialog = ReceiptDialog(receipt_text)
        receipt_dialog.exec_()

    def cancelPurchase(self):
        from src.Dashboard import Dashboard  # Importing inside the function to avoid circular import

        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)

    @pyqtSlot()
    def complete_purchase(self):

         # Check for expired items in the cart
        for row in range(self.ItemsTable.rowCount()):
            item_id = self.ItemsTable.item(row, 0).text().strip() if self.ItemsTable.item(row, 0) else ""
            
            if item_id and self.inventory.is_expired(item_id):  # Assuming is_expired method takes an item ID
                QMessageBox.warning(self, "Expiration Warning", f"The item {item_id} is expired and cannot be sold.")
                return  # Stop purchase if expired item is found

        first_name = self.FName.text()
        last_name = self.LName.text()
        payment_method = self.PaymentMethod.currentText()

        if not first_name or not last_name:
            QMessageBox.warning(self, "Input Error", "Please enter both first and last names.")
            return

        if self.check_for_prescription_items() and not self.show_signature_popup():
            return

        grand_total = self.grandTotalLabel.text()
        QMessageBox.information(self, "Purchase Complete", f"Purchase completed successfully.\n{grand_total}")

        # Save the purchase details to the purchase CSV
        self.save_to_csv(first_name, last_name, payment_method, grand_total)

        # Update the inventory based on the items purchased
        self.update_inventory_after_purchase()

        # Reset the table and clear fields
        self.reset_table()
        self.FName.clear()
        self.LName.clear()
        self.returnToDashboard()

    def update_inventory_after_purchase(self):
        """
        Update the db_inventory.csv file to reflect the purchased quantities.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        inventory_file = os.path.join(base_path, '..', 'DBFiles', 'db_inventory.csv')

        if not os.path.exists(inventory_file):
            QMessageBox.critical(self, "Error", "Inventory file not found.")
            return

        # Load the inventory data into a dictionary
        inventory = {}
        with open(inventory_file, mode='r') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                inventory[row['ID']] = row

        # Update the inventory quantities based on the items purchased
        for row in range(self.ItemsTable.rowCount()):
            item_id = self.ItemsTable.item(row, 1).text().strip() if self.ItemsTable.item(row, 1) else ""

            # Ignore rows where the ID is empty
            if not item_id:
                continue

            quantity_purchased_text = self.ItemsTable.item(row, 2).text() if self.ItemsTable.item(row, 2) else "0"

            try:
                quantity_purchased = int(quantity_purchased_text)
            except ValueError:
                quantity_purchased = 0  # Default to 0 if the value is invalid

            if item_id in inventory:
                try:
                    current_quantity = int(inventory[item_id]['Quantity'])
                except ValueError:
                    current_quantity = 0  # Default to 0 if the value is invalid in the CSV

                new_quantity = max(0, current_quantity - quantity_purchased)  # Ensure quantity doesn't go negative
                inventory[item_id]['Quantity'] = str(new_quantity)

        # Write the updated inventory back to the CSV
        with open(inventory_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory.values())


    def check_for_prescription_items(self):
        """Checks if any items in the cart are marked as 'yes' in the 'Prescription' column."""
        for row in range(self.ItemsTable.rowCount()):
            prescription_status = self.ItemsTable.item(row, 5).text().lower() if self.ItemsTable.item(row, 5) else "no"
            if prescription_status == "yes":
                return True
        return False

    def show_signature_popup(self):
        """Show a popup asking the user to confirm that they acknowledge the prescription medication."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Prescription Medication Confirmation")

        layout = QVBoxLayout(dialog)
        label = QLabel("Please acknowledge receipt of prescription medication.")
        layout.addWidget(label)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button)

        return dialog.exec_() == QDialog.Accepted



    def save_to_csv(self, first_name, last_name, payment_method, grand_total):
        # Construct the path to the CSV file
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get the base directory path
        file_path = os.path.join(base_path, '..', 'DBFiles', 'db_purchase_data.csv')  # Path to the CSV file

        # Ensure the CSV file exists
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write headers if the file doesn't exist yet
                writer.writerow(['Date', 'First Name', 'Last Name', 'Item Name', 'ID', 'Quantity', 'Price', 'Total Cost', 'Grand Total', 'Payment Method', 'Prescription'])

        # Extract only the numeric value from the grand total text (removes "Grand Total: $")
        grand_total_numeric = float(grand_total.replace("Grand Total: $", "").strip())

        # Get the current date in "YYYY-MM-DD" format
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Open the CSV file in append mode to add new data
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Collect all rows (item name, quantity, price, total cost)
            for row in range(self.ItemsTable.rowCount()):
                item_name = self.ItemsTable.item(row, 0).text() if self.ItemsTable.item(row, 0) else ""
                item_id = self.ItemsTable.item(row, 1).text() if self.ItemsTable.item(row, 1) else ""
                quantity = self.ItemsTable.item(row, 2).text() if self.ItemsTable.item(row, 2) else "0"
                price = self.ItemsTable.item(row, 3).text() if self.ItemsTable.item(row, 3) else "0.00"
                total_cost = self.ItemsTable.item(row, 4).text() if self.ItemsTable.item(row, 4) else "0.00"
                prescription_status = self.ItemsTable.item(row, 5).text().lower() if self.ItemsTable.item(row, 5) else "no"

                # Skip rows where the ID is empty
                if not item_id.strip():
                    continue

                # Write data for each item, including the current date and prescription status
                writer.writerow([current_date, first_name, last_name, item_name, item_id, quantity, price, total_cost, grand_total_numeric, payment_method, prescription_status])

    def reset_table(self):
        self.ItemsTable.setRowCount(4)
        for row in range(self.ItemsTable.rowCount()):
            for column in range(self.ItemsTable.columnCount()):
                self.ItemsTable.setItem(row, column, QTableWidgetItem(""))
        self.grandTotalLabel.setText("Grand Total: $0.00")

    def returnToDashboard(self):
        from src.Dashboard import Dashboard

        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Dashboard):
                self.widget.setCurrentIndex(i)
                return

        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))

    def update_grand_total(self, item=None):
        grand_total = 0.0
        self.ItemsTable.blockSignals(True)

        try:
            for row in range(self.ItemsTable.rowCount()):
                quantity_item = self.ItemsTable.item(row, 2)
                price_item = self.ItemsTable.item(row, 3)

                try:
                    quantity = int(quantity_item.text()) if quantity_item else 0
                    price = float(price_item.text()) if price_item else 0.0
                except ValueError:
                    quantity = 0
                    price = 0.0

                total_cost = quantity * price
                self.ItemsTable.setItem(row, 4, QTableWidgetItem(f"{total_cost:.2f}"))
                grand_total += total_cost

            self.grandTotalLabel.setText(f"Grand Total: ${grand_total:.2f}")
        finally:
            self.ItemsTable.blockSignals(False)

    def add_item(self):
        """
        Populate table rows based on the ID column from db_inventory.csv.
        Skip rows where the ID column is empty.
        """
        # Iterate through all rows in the table
        for row in range(self.ItemsTable.rowCount()):
            id_item = self.ItemsTable.item(row, 1)  # Assuming column 1 is ID

            # Skip the row if the ID column is empty or invalid
            if id_item is None or not id_item.text().strip():
                continue

            item_id = id_item.text().strip()

            # Read from db_inventory.csv
            base_path = os.path.dirname(os.path.abspath(__file__))
            inventory_file = os.path.join(base_path, '..', 'DBFiles', 'db_inventory.csv')

            if not os.path.exists(inventory_file):
                QMessageBox.critical(self, "Error", "Inventory file not found.")
                return

            # Look up the item in the inventory file
            item_found = False
            with open(inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row_data in reader:
                    if row_data['ID'] == item_id:
                        # Populate the table row with the item's details
                        self.ItemsTable.setItem(row, 0, QTableWidgetItem(row_data['Item']))  # Item Name
                        self.ItemsTable.setItem(row, 2, QTableWidgetItem("1"))  # Default Quantity to 1
                        self.ItemsTable.setItem(row, 3, QTableWidgetItem(row_data['Price']))  # Price
                        self.ItemsTable.setItem(row, 5, QTableWidgetItem("No"))  # Default Prescription Status
                        item_found = True
                        break

            # If the item was not found, clear the row's data and show a warning
            if not item_found:
                QMessageBox.warning(self, "Not Found", f"Item with ID {item_id} not found in inventory.")
                self.ItemsTable.setItem(row, 0, QTableWidgetItem(""))  # Clear Item Name
                self.ItemsTable.setItem(row, 2, QTableWidgetItem(""))  # Clear Quantity
                self.ItemsTable.setItem(row, 3, QTableWidgetItem(""))  # Clear Price
                self.ItemsTable.setItem(row, 5, QTableWidgetItem(""))  # Clear Prescription Status

        # Recalculate the total after adding/updating items
        self.update_grand_total()



    def remove_item(self):
        selected_items = self.ItemsTable.selectedItems()
        if selected_items:
            self.ItemsTable.removeRow(selected_items[0].row())
            self.update_grand_total()
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to remove.")


class ReceiptDialog(QDialog):
    def __init__(self, receipt_text, parent=None):
        super(ReceiptDialog, self).__init__(parent)
        self.setWindowTitle("Receipt")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout(self)

        receipt_display = QTextEdit()
        receipt_display.setReadOnly(True)
        receipt_display.setText(receipt_text)
        layout.addWidget(receipt_display)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
