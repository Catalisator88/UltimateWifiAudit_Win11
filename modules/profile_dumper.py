# modules/profile_dumper.py (Базовый)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from core.wifi_manager import WindowsWifiManager
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    print("[-] Не удалось импортировать WindowsWifiManager. Проверьте core/wifi_manager.py")

class ProfileDumper:
    def __init__(self):
        if HAS_CORE:
            self.wifi_manager = WindowsWifiManager()
        else:
            self.wifi_manager = None
    
    def get_saved_profiles(self, interface_index=0):
        """Возвращает список имён сохранённых профилей."""
        if not self.wifi_manager or not self.wifi_manager.interfaces:
            return []
        return self.wifi_manager.get_saved_profiles(interface_index)
    
    def run(self):
        """Основная функция для тестирования."""
        print("[ProfileDumper] Запуск теста...")
        profiles = self.get_saved_profiles()
        if profiles:
            print(f"[+] Найдено профилей: {len(profiles)}")
            for i, name in enumerate(profiles[:5], 1):
                print(f"  {i}. {name}")
            if len(profiles) > 5:
                print(f"  ... и ещё {len(profiles)-5}")
        else:
            print("[-] Профили не найдены или ошибка подключения к ядру.")

if __name__ == "__main__":
    dumper = ProfileDumper()
    dumper.run()