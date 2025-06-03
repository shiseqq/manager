from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import psutil

class SystemMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        
    def start(self):
        self.timer.start(1000)  # Обновление каждую секунду
        
    def update_stats(self):
        stats = {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "processes": len(psutil.pids())
        }
        self.stats_updated.emit(stats)