# modules/scanner.py (Базовый)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from core.wifi_manager import WindowsWifiManager
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    print("[-] Не удалось импортировать WindowsWifiManager. Проверьте core/wifi_manager.py")

class NetworkScanner:
    def __init__(self):
        if HAS_CORE:
            self.wifi_manager = WindowsWifiManager()
        else:
            self.wifi_manager = None
    
    def scan_networks(self, interface_index=0):
        """Сканирует сети через C# ядро."""
        if not self.wifi_manager or not self.wifi_manager.interfaces:
            return []
        return self.wifi_manager.scan_networks(interface_index)
    
    def run(self):
        """Основная функция для тестирования."""
        print("[NetworkScanner] Запуск сканирования...")
        networks = self.scan_networks()
        if networks:
            print(f"[+] Найдено сетей: {len(networks)}")
            for i, net in enumerate(networks[:5], 1):
                print(f"  {i}. {net}")
            if len(networks) > 5:
                print(f"  ... и ещё {len(networks)-5}")
        else:
            print("[-] Сети не найдены или ошибка сканирования.")

if __name__ == "__main__":
    scanner = NetworkScanner()
    scanner.run()