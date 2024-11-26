from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.uic import loadUi
import os
import csv
from PyQt5.QtCore import pyqtSlot
from datetime import datetime
from Inventory import Inventory


class Purchases(QMainWindow):
    def __init__(self, widget, username): # Accept the widget and username as arguments
        super(Purchases, self).__init__()
        self.widget = widget
        self.username = username
        
        # Initialize the inventory class
        self.inventory = Inventory()

        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Purchase.ui')
        loadUi(ui_path, self)

        # Set the window title
        self.setMinimumSize(1100, 600)
        self.grandTotalLabel.setText("Grand Total: $0.00")

        # Connect the buttons to their respective functions
        self.addItemButton.clicked.connect(self.add_item)
        self.removeItemButton.clicked.connect(self.remove_item)
        self.cancelButton.clicked.connect(self.cancelPurchase)
        self.Complete.clicked.connect(self.complete_purchase)
        self.PrintReciept.clicked.connect(self.print_receipt)
        self.ItemsTable.itemChanged.connect(self.update_grand_total)


    def print_receipt(self):
        # Create the receipt text
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

        # Create & show receipt
        receipt_dialog = ReceiptDialog(receipt_text)
        receipt_dialog.exec_()


    def cancelPurchase(self):
        # Takes the user back to the dashboard
        from src.Dashboard import Dashboard # Don't want circular imports here so import inside the function

        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)


    def complete_purchase(self):
        # Check for expired items in the cart
        for row in range(self.ItemsTable.rowCount()):
            item_id = self.ItemsTable.item(row, 0).text().strip() if self.ItemsTable.item(row, 0) else ""
            if item_id and self.inventory.is_expired(item_id):
                #warn user that the item is expired
                QMessageBox.warning(self, "Expiration Warning", f"The item {item_id} is expired and cannot be sold.")
                return

        # Check if the user has entered a first and last name and payment method
        first_name = self.FName.text()
        last_name = self.LName.text()
        payment_method = self.PaymentMethod.currentText()

        if not first_name or not last_name:
            # Notify the user if the first or last name is missing
            QMessageBox.warning(self, "Input Error", "Please enter both first and last names.")
            return

        if self.check_for_prescription_items() and not self.show_signature_popup():
            return

        grand_total = self.grandTotalLabel.text()
        QMessageBox.information(self, "Purchase Complete", f"Purchase completed successfully.\n{grand_total}")

        # Saving purchases details to purchase CSV
        self.save_to_csv(first_name, last_name, payment_method, grand_total)

        # Log the purchase action
        self.log_purchase()

        # Update the inventory based on the items purchased
        self.update_inventory_after_purchase()

        # Reset table
        self.reset_table()
        self.FName.clear()
        self.LName.clear()
        self.returnToDashboard()


    def log_purchase(self):
        # Log the purchase action to a file
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'transaction.log')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = self.username

        # Format the log entry
        log_entry = f"{timestamp} - USER: {username} - ACTION: PURCHASE\n"

        # Write the log entry to the file
        try:
            with open(log_file, mode='a') as file:
                file.write(log_entry)
        except Exception as e:
            # Notify the user if the log file write fails
            QMessageBox.critical(self, "Error", f"Failed to write to log file: {e}")


    def update_inventory_after_purchase(self):
        # Update the inventory quantities after a purchase
        base_path = os.path.dirname(os.path.abspath(__file__))
        inventory_file = os.path.join(base_path, '..', 'DBFiles', 'db_inventory.csv')

        if not os.path.exists(inventory_file):
            # Notify the user if the inventory file is missing
            QMessageBox.critical(self, "Error", "Inventory file not found.")
            return

        # Load the inventory data into a dictionary
        inventory = {}
        
        # Read the inventory data from the CSV file
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
                # Convert the quantity to an integer
                quantity_purchased = int(quantity_purchased_text)
            except ValueError:
                # Set the quantity to 0 if it's not a valid number
                quantity_purchased = 0

            if item_id in inventory:
                try:
                    # Subtract the purchased quantity from the current quantity
                    current_quantity = int(inventory[item_id]['Quantity'])
                except ValueError:
                    current_quantity = 0

                # Ensure the new quantity is not negative
                new_quantity = max(0, current_quantity - quantity_purchased)
                inventory[item_id]['Quantity'] = str(new_quantity)

        # Write the updated inventory back to the CSV
        with open(inventory_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory.values())


    def check_for_prescription_items(self):
        # Checks if any items in the cart are marked as 'yes' in the 'Prescription' column
        for row in range(self.ItemsTable.rowCount()):
            prescription_status = self.ItemsTable.item(row, 5).text().lower() if self.ItemsTable.item(row, 5) else "no"
            if prescription_status == "yes":
                return True
        return False

    def show_signature_popup(self):
        # Show a dialog to confirm the receipt of prescription medication
        dialog = QDialog(self)
        dialog.setWindowTitle("Prescription Medication Confirmation")

        # Create a layout for the dialog
        layout = QVBoxLayout(dialog)
        label = QLabel("Please acknowledge receipt of prescription medication.")
        layout.addWidget(label)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button)

        # Return True if the dialog is accepted, False otherwise
        return dialog.exec_() == QDialog.Accepted


    def save_to_csv(self, first_name, last_name, payment_method, grand_total):
        # Save the purchase details to a CSV file
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, '..', 'DBFiles', 'db_purchase_data.csv')

        # does csv exist?
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write headers if the file doesn't exist yet
                writer.writerow(['Date', 'First Name', 'Last Name', 'Item Name', 'ID', 'Quantity', 'Price', 'Total Cost', 'Grand Total', 'Payment Method', 'Prescription'])

        # Extract the numeric value from the grand total string
        grand_total_numeric = float(grand_total.replace("Grand Total: $", "").strip())

        # Get the current date in the format YYYY-MM-DD
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Open the CSV file in append mode to add new data
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Collect all rows
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

                # Write data for each item
                writer.writerow([current_date, first_name, last_name, item_name, item_id, quantity, price, total_cost, grand_total_numeric, payment_method, prescription_status])


    def reset_table(self):
        # Clear all items in the table
        self.ItemsTable.setRowCount(4)
        for row in range(self.ItemsTable.rowCount()):
            for column in range(self.ItemsTable.columnCount()):
                self.ItemsTable.setItem(row, column, QTableWidgetItem(""))
        self.grandTotalLabel.setText("Grand Total: $0.00")


    def returnToDashboard(self):
        # return to the dashboard
        from src.Dashboard import Dashboard # Import here to avoid circular imports

        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Dashboard):
                self.widget.setCurrentIndex(i)
                return

        # If the dashboard is not found, create a new instance
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))


    def update_grand_total(self, item=None):
        # Update the grand total based on the items in the table
        grand_total = 0.0
        self.ItemsTable.blockSignals(True)

        try:
            # Iterate through each row in the table
            for row in range(self.ItemsTable.rowCount()):
                quantity_item = self.ItemsTable.item(row, 2)
                price_item = self.ItemsTable.item(row, 3)

                try:
                    # Convert the quantity and price to integers and floats, respectively
                    quantity = int(quantity_item.text()) if quantity_item else 0
                    price = float(price_item.text()) if price_item else 0.0
                except ValueError:
                    quantity = 0
                    price = 0.0

                # Calculate the total cost for the item
                total_cost = quantity * price
                self.ItemsTable.setItem(row, 4, QTableWidgetItem(f"{total_cost:.2f}"))
                grand_total += total_cost

            self.grandTotalLabel.setText(f"Grand Total: ${grand_total:.2f}")
        finally:
            # Unblock the signals to allow itemChanged to be triggered
            self.ItemsTable.blockSignals(False)


    def add_item(self):
        # Iterate through all rows in the table
        for row in range(self.ItemsTable.rowCount()):
            id_item = self.ItemsTable.item(row, 1)

            # Skip the row if the ID column is empty or invalid
            if id_item is None or not id_item.text().strip():
                continue

            item_id = id_item.text().strip()

            # Read from db_inventory.csv
            base_path = os.path.dirname(os.path.abspath(__file__))
            inventory_file = os.path.join(base_path, '..', 'DBFiles', 'db_inventory.csv')

            if not os.path.exists(inventory_file):
                # Notify the user if the inventory file is missing
                QMessageBox.critical(self, "Error", "Inventory file not found.")
                return

            # Look up the item in the inventory file
            item_found = False
            with open(inventory_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row_data in reader:
                    if row_data['ID'] == item_id:
                        # Populate the table row with the item's details
                        self.ItemsTable.setItem(row, 0, QTableWidgetItem(row_data['Item']))  
                        self.ItemsTable.setItem(row, 2, QTableWidgetItem("1"))  
                        self.ItemsTable.setItem(row, 3, QTableWidgetItem(row_data['Price']))
                        self.ItemsTable.setItem(row, 5, QTableWidgetItem("No"))
                        item_found = True
                        break

            # If the item was not found, clear the row's data and show a warning
            if not item_found:
                QMessageBox.warning(self, "Not Found", f"Item with ID {item_id} not found in inventory.")
                self.ItemsTable.setItem(row, 0, QTableWidgetItem(""))
                self.ItemsTable.setItem(row, 2, QTableWidgetItem(""))
                self.ItemsTable.setItem(row, 3, QTableWidgetItem(""))
                self.ItemsTable.setItem(row, 5, QTableWidgetItem(""))

        # Recalculate the total after adding/updating items
        self.update_grand_total()


    def remove_item(self):
        # Remove the selected row from the table
        selected_items = self.ItemsTable.selectedItems()
        if selected_items:
            # Remove the selected row
            self.ItemsTable.removeRow(selected_items[0].row())
            self.update_grand_total()
        else:
            # Notify the user if no row is selected
            QMessageBox.warning(self, "Warning", "Please select a row to remove.")


class ReceiptDialog(QDialog):
    def __init__(self, receipt_text, parent=None): # Accept the receipt text and parent as an argument
        super(ReceiptDialog, self).__init__(parent)
        
        # Set the window title and size
        self.setWindowTitle("Receipt")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout(self)

        # Create a QTextEdit widget to display the receipt text
        receipt_display = QTextEdit()
        receipt_display.setReadOnly(True)
        receipt_display.setText(receipt_text)
        layout.addWidget(receipt_display)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)