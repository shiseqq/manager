import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui import MainWindow

def handle_exception(exc_type, exc_value, exc_traceback):
    """Перехват всех необработанных исключений."""
    QMessageBox.critical(
        None,
        "Ошибка",
        f"Произошла ошибка:\n{exc_value}",
        QMessageBox.StandardButton.Ok
    )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def main():
    sys.excepthook = handle_exception  # Перехват ошибок
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()