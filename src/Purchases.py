from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.uic import loadUi
import os
import csv
from PyQt5.QtCore import pyqtSlot


class Purchases(QMainWindow):
    def __init__(self, widget, username):  # Accept the widget as an argument
        super(Purchases, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference
        self.username = username  # Store the username

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Purchase.ui')
        loadUi(ui_path, self)
        # Set a minimum size for the dashboard
        self.setMinimumSize(1100, 600)  # Example size, you can adjust these values
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
            quantity = self.ItemsTable.item(row, 1).text() if self.ItemsTable.item(row, 1) else "0"
            price = self.ItemsTable.item(row, 2).text() if self.ItemsTable.item(row, 2) else "0.00"
            total = self.ItemsTable.item(row, 3).text() if self.ItemsTable.item(row, 3) else "0.00"

            # Format each row for the receipt.
            receipt_text += "{:<15} {:<10} {:<10} {:<10}\n".format(item, quantity, price, total)

        receipt_text += "-" * 40 + "\n"
        receipt_text += f"Payment Method: {self.PaymentMethod.currentText()}\n"  # Added payment method to receipt
        receipt_text += f"{self.grandTotalLabel.text()}\n"
        receipt_text += "-" * 40 + "\n"

        # Create and show the receipt dialog.
        receipt_dialog = ReceiptDialog(receipt_text)
        receipt_dialog.exec_()  # Show as a modal dialog

    def cancelPurchase(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)

    @pyqtSlot()
    def complete_purchase(self):
        # Collect customer details
        first_name = self.FName.text()  # Assuming a line edit for first name
        last_name = self.LName.text()   # Assuming a line edit for last name
        payment_method = self.PaymentMethod.currentText()  # Assuming a combo box for payment method
        
        # Check if first name or last name is empty
        if not first_name or not last_name:
            QMessageBox.warning(self, "Input Error", "Please enter both first and last names.")
            return  # Stop further execution if fields are empty
        
        # Before completing, check if any prescription medication is being purchased
        if self.check_for_prescription_items():
            # Show confirmation dialog for signature before completing purchase
            confirmation = self.show_signature_popup()
            if not confirmation:
                return  # If the user doesn't acknowledge, don't proceed with the purchase
        
        # Show a confirmation message box
        grand_total = self.grandTotalLabel.text()
        msg = QMessageBox()
        msg.setWindowTitle("Purchase Complete")
        msg.setText(f"Purchase completed successfully.\n{grand_total}")
        msg.setStandardButtons(QMessageBox.Ok)

        # If user clicks OK, save to CSV, reset table, and clear name fields
        if msg.exec_() == QMessageBox.Ok:
            self.save_to_csv(first_name, last_name, payment_method, grand_total)
            self.reset_table()  # Reset the table to 4 rows before returning
            self.returnToDashboard()
            
            # Clear the first name and last name fields
            self.FName.clear()  # Clear the first name field
            self.LName.clear()  # Clear the last name field

    def check_for_prescription_items(self):
        """
        Checks if any items in the cart are marked as 'yes' in the 'Prescription' column.
        """
        for row in range(self.ItemsTable.rowCount()):
            prescription_status = self.ItemsTable.item(row, 4).text().lower()
            if prescription_status == "yes":
                return True
        return False

    def show_signature_popup(self):
        """
        Show a popup asking the user to confirm that they acknowledge the prescription medication.
        This is essentially a confirmation dialog for the 'signature' requirement.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Prescription Medication Confirmation")
        
        layout = QVBoxLayout(dialog)
        label = QLabel("Please acknowledge that you have received prescription medication at the point of sale.")
        layout.addWidget(label)
        
        # Add a 'Confirm' button
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button)

        # Show the dialog and wait for user confirmation
        return dialog.exec_() == QDialog.Accepted  # Return True if confirmed, False if canceled

    def save_to_csv(self, first_name, last_name, payment_method, grand_total):
        # Construct the path to the CSV file, changing the name to db_purchase_data.csv
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get the base directory path
        file_path = os.path.join(base_path, '..', 'DBFiles', 'db_purchase_data.csv')  # Path to the CSV file

        # Ensure the CSV file exists
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write headers if the file doesn't exist yet
                writer.writerow(['First Name', 'Last Name', 'Item Name', 'Quantity', 'Price', 'Total Cost', 'Grand Total', 'Payment Method', 'Prescription'])

        # Extract only the numeric value from the grand total text (removes "Grand Total: $")
        grand_total_numeric = float(grand_total.replace("Grand Total: $", "").strip())  # Convert to float

        # Open the CSV file in append mode to add new data
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Collect all rows (item name, quantity, price, total cost)
            for row in range(self.ItemsTable.rowCount()):
                item_name = self.ItemsTable.item(row, 0).text() if self.ItemsTable.item(row, 0) else ""
                quantity = self.ItemsTable.item(row, 1).text() if self.ItemsTable.item(row, 1) else "0"
                price = self.ItemsTable.item(row, 2).text() if self.ItemsTable.item(row, 2) else "0.00"
                total_cost = self.ItemsTable.item(row, 3).text() if self.ItemsTable.item(row, 3) else "0.00"
                prescription_status = self.ItemsTable.item(row, 4).text().lower() if self.ItemsTable.item(row, 4) else "no"
                
                # Write data for each item, including the prescription status
                writer.writerow([first_name, last_name, item_name, quantity, price, total_cost, grand_total_numeric, payment_method, prescription_status])

    def reset_table(self):
        """Reset the table to 4 rows with no data."""
        self.ItemsTable.setRowCount(4)  # Set number of rows to 4
        
        # Clear all the cells in the table
        for row in range(self.ItemsTable.rowCount()):
            for column in range(self.ItemsTable.columnCount()):
                self.ItemsTable.setItem(row, column, QTableWidgetItem(""))  # Clear the cell contents

        self.grandTotalLabel.setText("Grand Total: $0.00")  # Reset the grand total label

    def returnToDashboard(self):
        from src.Dashboard import Dashboard

        # Check if the dashboard is already in the stacked widget
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Dashboard):
                self.widget.setCurrentIndex(i)  # Switch to existing Dashboard
                return

        # If not found, create the dashboard and add it to the stacked widget
        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))

    def update_grand_total(self, item=None):
        grand_total = 0.0

        # Temporarily disconnect the signal to avoid recursion.
        self.ItemsTable.blockSignals(True)

        try:
            # Calculate total for all rows in the table.
            for row in range(self.ItemsTable.rowCount()):
                quantity_item = self.ItemsTable.item(row, 1)  # Assuming 2nd column is Quantity
                price_item = self.ItemsTable.item(row, 2)     # Assuming 3rd column is Price

                try:
                    quantity = int(quantity_item.text()) if quantity_item else 0
                    price = float(price_item.text()) if price_item else 0.0
                except ValueError:
                    quantity = 0
                    price = 0.0

                # Calculate total cost for each row.
                total_cost = quantity * price

                # Update the total cost in the 4th column (index 3) for the row that was changed
                self.ItemsTable.setItem(row, 3, QTableWidgetItem(f"{total_cost:.2f}"))

                # Add to grand total.
                grand_total += total_cost

            # Update the grand total label.
            self.grandTotalLabel.setText(f"Grand Total: ${grand_total:.2f}")
        finally:
            # Reconnect the signal after updating.
            self.ItemsTable.blockSignals(False)

    def add_item(self):
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)

    def remove_item(self):
        selected_items = self.ItemsTable.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            self.ItemsTable.removeRow(selected_row)
            self.update_grand_total()
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to remove.")


class ReceiptDialog(QDialog):
    def __init__(self, receipt_text, parent=None):
        super(ReceiptDialog, self).__init__(parent)
        self.setWindowTitle("Receipt")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout(self)

        # Use a QTextEdit to display the receipt text.
        receipt_display = QTextEdit()
        receipt_display.setReadOnly(True)
        receipt_display.setText(receipt_text)
        layout.addWidget(receipt_display)

        # Add a Close button.
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
