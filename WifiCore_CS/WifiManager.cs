# core/wifi_manager.py
import clr
import sys
import os
from typing import List, Optional

# Добавляем путь к нашей DLL
dll_path = os.path.join(os.path.dirname(__file__), '..', 'WifiCore.dll')
clr.AddReference(dll_path)

# Импортируем наш C# класс
from WifiCore import WifiManager

class WindowsWifiManager:
    """Обёртка для C# класса WifiManager."""
    
    def __init__(self):
        try:
            self.wifi_core = WifiManager()
            print("[+] C# ядро WifiManager успешно загружено")
        except Exception as e:
            print(f"[-] Ошибка загрузки C# ядра: {e}")
            self.wifi_core = None
    
    def get_interface_names(self) -> List[str]:
        """Возвращает список описаний WiFi интерфейсов (заменяет старый метод)."""
        if not self.wifi_core:
            return []
        return list(self.wifi_core.GetInterfaceNames())
    
    def scan_networks(self, interface_index: int = 0) -> List[str]:
        """Сканирует сети на выбранном интерфейсе (interface_index пока игнорируем)."""
        if not self.wifi_core:
            return []
        return list(self.wifi_core.ScanNetworks())
    
    # ИСПРАВЛЕНИЕ: Переименовываем метод для соответствия GUI
    def get_saved_profiles(self, interface_index: int = 0) -> List[str]:
        """Возвращает список сохранённых WiFi профилей (interface_index игнорируем)."""
        if not self.wifi_core:
            return []
        return list(self.wifi_core.GetProfiles())
    
    # Новый метод для получения пароля (для будущего использования)
    def get_profile_password(self, profile_name: str) -> str:
        """Возвращает пароль для указанного профиля."""
        if not self.wifi_core:
            return "Ядро не загружено"
        return self.wifi_core.GetProfilePassword(profile_name)

# Быстрый тест
if __name__ == "__main__":
    manager = WindowsWifiManager()
    print("Интерфейсы:", manager.get_interface_names())
    print("\nСканирование сетей...")
    networks = manager.scan_networks()
    for net in networks[:3]:
        print(" ", net)
    print("\nПрофили:")
    profiles = manager.get_saved_profiles()
    for profile in profiles[:5]:
        print(" ", profile)