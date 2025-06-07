import socket
import threading
from PyQt6.QtCore import QObject, pyqtSignal

class NetworkScanner(QObject):
    computers_found = pyqtSignal(list)

    def __init__(self, ip_range="192.168.1.1-100"):
        super().__init__()
        self.ip_range = ip_range
        self.running = False

    def scan_network(self):
        self.running = True
        active_hosts = []
        start_ip, end_ip = self._parse_ip_range()
        
        threads = []
        for i in range(start_ip, end_ip + 1):
            ip = f"192.168.1.{i}"
            thread = threading.Thread(target=self._check_host, args=(ip, active_hosts))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        self.computers_found.emit(active_hosts)
        self.running = False

    def _parse_ip_range(self):
        start, end = map(int, self.ip_range.split('-'))
        return start, end

    def _check_host(self, ip, active_hosts):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            active_hosts.append((ip, hostname))
            socket.setdefaulttimeout(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 3389))  # Проверяем RDP порт (можно изменить)
            s.close()
            active_hosts.append(ip)
        except:
            pass