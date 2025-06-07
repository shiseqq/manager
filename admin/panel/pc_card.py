from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, 
    QPushButton, QMessageBox, QInputDialog, 
    QDialog, QHBoxLayout, QLineEdit
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
            border: 1px solid #ccc;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
        QMessageBox QLabel {
            margin-left: 50px;
            padding-left: 0px;
            text-align: left;
        }
    """
    
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address  # Сохраняем IP адрес
        self.custom_name = f"PC-{ip_address.split('.')[-1]}"  # Генерируем имя
        self.is_locked = True
        self.time_left = 0
        
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.init_ui()
        self.update_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        
        # Верхняя строка с именем и кнопкой редактирования
        self.name_layout = QHBoxLayout()
        
        # Поле для отображения имени
        self.name_label = QLabel(self.custom_name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: black;")
        
        # Поле для редактирования имени (изначально скрыто)
        self.name_edit = QLineEdit(self.custom_name)
        self.name_edit.setHidden(True)
        self.name_edit.returnPressed.connect(self.save_name)
        
        # Кнопка редактирования имени
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(24, 24)
        self.edit_btn.setStyleSheet("border: none; background: transparent;")
        self.edit_btn.clicked.connect(self.toggle_name_edit)
        
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_edit)
        self.name_layout.addWidget(self.edit_btn)
        
        self.layout.addLayout(self.name_layout)
        
        # Статус
        self.status = QLabel()
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Таймер
        self.timer_label = QLabel("Время: 00:00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("color: black;")
        
        # Кнопка управления сеансом
        self.action_btn = QPushButton()
        self.action_btn.clicked.connect(self.handle_action)
        
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.action_btn)
        self.setLayout(self.layout)
        
        # Таймер обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
    
    def toggle_name_edit(self):
        """Переключает режим редактирования имени"""
        if self.name_edit.isHidden():
            self.name_label.setHidden(True)
            self.name_edit.setHidden(False)
            self.name_edit.setFocus()
            self.name_edit.setStyleSheet(self.DIALOG_STYLE)
        else:
            self.save_name()
    
    def save_name(self):
        """Сохраняет новое имя компьютера"""
        new_name = self.name_edit.text().strip()
        if new_name:
            self.custom_name = new_name
            self.name_label.setText(new_name)
        
        self.name_edit.setHidden(True)
        self.name_label.setHidden(False)
    
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
        msg_box.setText(f"Завершить сеанс на {self.custom_name}?")  # Используем кастомное имя
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.is_locked = True
            self.time_left = 0
            self.update_ui()

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value
        self.update_display()

    def update_display(self):
        self.title.setText(f"{self.custom_name} ({self.ip_address})")