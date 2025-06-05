from PyQt6.QtWidgets import QApplication
from window import AdminWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()