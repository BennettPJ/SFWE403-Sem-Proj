from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget
import sys
from src.LogInGUI import MainUI  # Import MainUI from LogInGUI.py in the src folder

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication instance is created here

    # Create the QStackedWidget
    widget = QStackedWidget()

    # Create the main window (login UI) and pass the widget to it
    mainwindow = MainUI(widget)
    widget.addWidget(mainwindow)

    # Get screen size using QDesktopWidget
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()

    # Get the size of the window from the designer (set by you in PyQt5 Designer)
    window_width = mainwindow.width()
    window_height = mainwindow.height()

    # Move the window to the center of the screen
    widget.resize(window_width, window_height)  # Keep the size from Designer
    widget.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)  # Center the window

    widget.show()

    # Execute the app
    sys.exit(app.exec_())  # Exit the app when the main loop ends
