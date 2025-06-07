from PyQt6.QtWidgets import (QMainWindow, QScrollArea, QWidget, 
                            QGridLayout, QLabel, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from core.network_scanner import NetworkScanner
from .pc_card import PCCard
import threading

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Админ-панель компьютерного клуба")
        self.resize(800, 600)
        
        self.scanner = NetworkScanner()
        self.scanner.computers_found.connect(self.update_computers_list)
        
        self.init_ui()
        self.start_scanning()

    def init_ui(self):
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        self.container = QWidget()
        self.layout = QGridLayout(self.container)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по имени или IP...")
        self.search_input.textChanged.connect(self.filter_computers)
        self.layout.addWidget(self.search_input, 0, 0, 1, 4)
        
        # Кнопка обновления
        self.refresh_btn = QPushButton("Обновить список")
        self.refresh_btn.clicked.connect(self.start_scanning)
        self.layout.addWidget(self.refresh_btn, 0, 4, 1, 2)
        
        self.scroll.setWidget(self.container)
        self.setCentralWidget(self.scroll)

    def filter_computers(self, text):
        """Фильтрация компьютеров по введенному тексту"""
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, PCCard):
                search_text = text.lower()
                matches_ip = search_text in widget.ip_address.lower()
                matches_name = search_text in widget.custom_name.lower()
                widget.setVisible(matches_ip or matches_name)

    def start_scanning(self):
        if not self.scanner.running:
            threading.Thread(target=self.scanner.scan_network).start()

    def update_computers_list(self, computers):
        # Очищаем старые карточки (кроме элементов управления)
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, PCCard):
                widget.deleteLater()
        
        # Добавляем новые компьютеры
        for i, (ip, hostname) in enumerate(computers):
            row = (i // 4) + 1  # 4 колонки
            col = i % 4
            pc_card = PCCard(ip)
            pc_card.custom_name = hostname  # Устанавливаем имя хоста
            self.layout.addWidget(pc_card, row, col)

    def closeEvent(self, event):
        self.scanner.running = False
        super().closeEvent(event)