from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.uic import loadUi
import os
import sys
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

    @pyqtSlot()
    def complete_purchase(self):
        grand_total = self.grandTotalLabel.text()

        # Show a confirmation message box
        msg = QMessageBox()
        msg.setWindowTitle("Purchase Complete")
        msg.setText(f"Purchase completed successfully.\n{grand_total}")
        msg.setStandardButtons(QMessageBox.Ok)

        # Connect the button click to return to the dashboard
        if msg.exec_() == QMessageBox.Ok:
            self.reset_table()  # Reset the table before returning
            self.returnToDashboard()

    def reset_table(self):
        """Clear all items from the ItemsTable while keeping the rows."""
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
            # Iterate through each row to calculate the total cost of each item.
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

                # Update the total cost in the 4th column (index 3).
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
