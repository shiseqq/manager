from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, 
    QProgressBar, QTabWidget,
    QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from monitoring import SystemMonitor
from pyqtgraph import PlotWidget, plot
import psutil

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer Club Manager v1.0")
        self.resize(600, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        
        # Вкладки
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Вкладка мониторинга
        self.create_monitor_tab()
        
        # Вкладка процессов
        self.create_processes_tab()
        
        # Инициализация мониторинга
        self.init_monitoring()

        # Графики
        self.create_graph_tab()
        self.history = {'cpu': [], 'ram': []}  # Хранение данных
        

    def create_monitor_tab(self):
        monitor_tab = QWidget()
        monitor_layout = QVBoxLayout()
        monitor_tab.setLayout(monitor_layout)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setFormat("CPU: %v%")
        
        self.ram_bar = QProgressBar()
        self.ram_bar.setFormat("RAM: %v%")
        
        monitor_layout.addWidget(self.cpu_bar)
        monitor_layout.addWidget(self.ram_bar)
        self.tabs.addTab(monitor_tab, "Мониторинг")

    def create_processes_tab(self):
        processes_tab = QWidget()
        self.processes_list = QListWidget()
        self.processes_list.itemDoubleClicked.connect(self.kill_process)
        processes_layout = QVBoxLayout()
        processes_layout.addWidget(self.processes_list)
        processes_tab.setLayout(processes_layout)
        self.tabs.addTab(processes_tab, "Процессы")

    def kill_process(self, item):
        pid = int(item.text().split(":")[0])
        try:
            process = psutil.Process(pid)
            process.terminate()
            self.update_processes()  # Обновляем список
        except Exception as e:
            print(f"Ошибка: {e}")

    def init_monitoring(self):
        # Мониторинг ресурсов
        self.monitor = SystemMonitor()
        self.monitor.stats_updated.connect(self.update_stats)
        self.monitor.start()
        
        # Таймер для процессов
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.update_processes)
        self.process_timer.start(2000)  # Обновлять каждые 2 секунды

    def update_stats(self, stats):
        self.cpu_bar.setValue(int(stats["cpu"]))
        self.ram_bar.setValue(int(stats["ram"]))
        
        # Динамическое изменение цвета
        self.update_bar_color(self.cpu_bar, stats["cpu"])
        self.update_bar_color(self.ram_bar, stats["ram"])

        self.history['cpu'].append(stats['cpu'])
        self.history['ram'].append(stats['ram'])
        
        # Ограничиваем историю 300 точками (5 минут при обновлении раз в секунду)
        for key in self.history:
            if len(self.history[key]) > 300:
                self.history[key] = self.history[key][-300:]
        
        # Обновляем графики
        self.update_plots()

        if stats['cpu'] > 90:
            self.show_alert("Внимание!", f"Высокая загрузка CPU: {stats['cpu']}%")
        if stats['ram'] > 90:
            self.show_alert("Внимание!", f"Мало свободной RAM: {stats['ram']}%")

    def update_bar_color(self, bar, value):
        color = "red" if value > 80 else "orange" if value > 50 else "green"
        bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
                width: 10px;
            }}
            QProgressBar {{
                text-align: center;
            }}
        """)

    def update_processes(self):
        self.processes_list.clear()
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                self.processes_list.addItem(
                    f"{proc.info['pid']}: {proc.info['name']} (CPU: {proc.info['cpu_percent']:.1f}%)"
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def create_graph_tab(self):
        graph_tab = QWidget()
        layout = QVBoxLayout()
        
        self.cpu_plot = PlotWidget(title="CPU Usage (%)")
        self.ram_plot = PlotWidget(title="RAM Usage (%)")
        
        layout.addWidget(self.cpu_plot)
        layout.addWidget(self.ram_plot)
        graph_tab.setLayout(layout)
        self.tabs.addTab(graph_tab, "Графики")

    def update_plots(self):
        self.cpu_plot.clear()
        self.ram_plot.clear()
        
        self.cpu_plot.plot(self.history['cpu'], pen='r')
        self.ram_plot.plot(self.history['ram'], pen='b')

    def show_alert(self, title, message):
        alert = QMessageBox()
        alert.setWindowTitle(title)
        alert.setText(message)
        alert.exec()