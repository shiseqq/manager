from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, 
    QPushButton, QMessageBox, QInputDialog, 
    QDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

class PCCard(QFrame):
    DIALOG_STYLE = """
            * {
                color: black !important;
            }
            QSpinBox, QPushButton {
                background-color: white;
                border: 1ps solid #ccc;
                padding: 5px
            }
            QPushButton:hover{
                background-color: #f0f0f0;
            }
            QMessageBox QLable{
                margin-left: 50px;
                padding-left: 0px;
                text-align: left;
            }
        """
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
        self.title.setStyleSheet("font-weight: bold; font-size: 14px; color: black;")
        
        # Статус
        self.status = QLabel()
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Таймер
        self.timer_label = QLabel("Время: 00:00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("color: black;")
        
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
            self.action_btn.setStyleSheet("background: #C8E6C9; color: black;")
            self.timer.stop()
        else:
            self.setStyleSheet("background: #E8F5E9;")
            self.status.setText("🟢 Сеанс активен")
            self.status.setStyleSheet("color: green;")
            self.action_btn.setText("Завершить сеанс")
            self.action_btn.setStyleSheet("background: #FFCDD2; color: black;")
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
        # Создаем кастомный диалог
        dialog = QInputDialog(self)
        dialog.setStyleSheet(self.DIALOG_STYLE)
        dialog.setWindowTitle("Начало сеанса")
        dialog.setLabelText("Длительность (минуты):")
        dialog.setIntValue(60)
        dialog.setIntMinimum(1)
        dialog.setIntMaximum(999999)
        dialog.setIntStep(5)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            mins = dialog.intValue()
            self.is_locked = False
            self.time_left = mins * 60
            self.update_ui()
    
    def end_session(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(self.DIALOG_STYLE)
        msg_box.setPalette(self.palette())
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText(f"Завершить сеанс на {self.pc_id}?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.is_locked = True
            self.time_left = 0
            self.update_ui()