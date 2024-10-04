from PyQt5.QtWidgets import QApplication  # Import QApplication
import sys
from src.LogInGUI import MainUI  # Import MainUI from LogInGUI.py in the src folder
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication instance is created here

    # Create the QStackedWidget
    widget = QtWidgets.QStackedWidget()

    # Create the main window (login UI) and pass the widget to it
    mainwindow = MainUI(widget)
    widget.addWidget(mainwindow)

    # Set the window size and show it
    widget.setFixedWidth(1150)
    widget.setFixedHeight(600)
    widget.show()

    # Execute the app
    sys.exit(app.exec_())  # Exit the app when the main loop ends
