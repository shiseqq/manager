from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, 
    QPushButton, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

class PCCard(QFrame):
    def __init__(self, pc_id):
        super().__init__()
        self.pc_id = pc_id
        self.is_locked = True
        self.time_left = 0
        
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.init_ui()
        self.update_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        
        # Заголовок с ID
        self.title = QLabel(f"Компьютер {self.pc_id}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        # Статус
        self.status = QLabel()
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Таймер
        self.timer_label = QLabel("Время: 00:00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка
        self.action_btn = QPushButton()
        self.action_btn.clicked.connect(self.handle_action)
        
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.action_btn)
        self.setLayout(self.layout)
        
        # Таймер обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
    
    def update_ui(self):
        if self.is_locked:
            self.setStyleSheet("background: #FFEBEE;")
            self.status.setText("🔴 Заблокирован")
            self.status.setStyleSheet("color: red;")
            self.action_btn.setText("Начать сеанс")
            self.action_btn.setStyleSheet("background: #C8E6C9;")
            self.timer.stop()
        else:
            self.setStyleSheet("background: #E8F5E9;")
            self.status.setText("🟢 Сеанс активен")
            self.status.setStyleSheet("color: green;")
            self.action_btn.setText("Завершить сеанс")
            self.action_btn.setStyleSheet("background: #FFCDD2;")
            self.timer.start(1000)
        
        self.update_timer()
    
    def update_timer(self):
        if not self.is_locked and self.time_left > 0:
            self.time_left -= 1
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            self.timer_label.setText(f"Время: {hours:02d}:{minutes:02d}:{seconds:02d}")
        elif self.time_left <= 0 and not self.is_locked:
            self.is_locked = True
            self.update_ui()
    
    def handle_action(self):
        if self.is_locked:
            self.start_session()
        else:
            self.end_session()
    
    def start_session(self):
        mins, ok = QInputDialog.getInt(
            self,
            "Начало сеанса",
            "Длительность (минуты):",
            value=60,
            min=1,
            max=999999,
            step=5
        )
        
        if ok and mins > 0:
            self.is_locked = False
            self.time_left = mins * 60
            self.update_ui()
    
    def end_session(self):
        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            f"Завершить сеанс на PC-{self.pc_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.is_locked = True
            self.time_left = 0
            self.update_ui()