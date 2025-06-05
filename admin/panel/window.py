from PyQt6.QtWidgets import (
    QMainWindow, QScrollArea, QWidget, 
    QGridLayout, QLabel
)
from PyQt6.QtCore import Qt
from pc_card import PCCard

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Админ-панель компьютерного клуба")
        self.resize(800, 600)
        
        # Основной скроллируемый виджет
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Контейнер для карточек
        container = QWidget()
        self.layout = QGridLayout(container)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title = QLabel("Мониторинг компьютеров")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title, 0, 0, 1, 2)
        
        # Добавляем компьютеры (4 колонки)
        for i in range(1, 13):  # 12 компьютеров для примера
            row = (i - 1) // 4 + 1
            col = (i - 1) % 4
            self.layout.addWidget(PCCard(f"PC-{i}"), row, col)
        
        scroll.setWidget(container)
        self.setCentralWidget(scroll)