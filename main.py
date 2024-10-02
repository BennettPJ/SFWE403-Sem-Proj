from PyQt5.QtWidgets import QApplication
import sys
from src.LogInGUI import MainUI  # Import MainUI from LogInGUI.py in the src folder

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec_())
