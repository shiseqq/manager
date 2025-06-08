# main.py
from PyQt6.QtWidgets import QApplication
from window import AdminWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())