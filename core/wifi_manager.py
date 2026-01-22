import os
import clr
import sys
from typing import List, Optional

# Подключаем твою скомпилированную DLL
dll_path = os.path.abspath("WifiCore.dll")
if os.path.exists(dll_path):
    try:
        clr.AddReference(dll_path)
        from WifiCore import WifiManager as InternalWifiManager
    except Exception as e:
        print(f"Ошибка загрузки WifiCore.dll: {e}")
        InternalWifiManager = None
else:
    InternalWifiManager = None

class WindowsWifiManager:

    def scan_networks(self, event=None) -> List[str]:
        """Псевдоним для совместимости с GUI и обработки события нажатия кнопки."""
        return self.scan_results()

    def __init__(self):
        self._manager = InternalWifiManager() if InternalWifiManager else None
        # GUI ожидает список имен при инициализации
        self.interfaces = self.get_interface_names()

    def get_interface_names(self) -> List[str]:
        if not self._manager:
            return ["Ядро не загружено"]
        try:
            # Вызываем метод из твоего C# кода
            return list(self._manager.GetInterfaceNames())
        except Exception as e:
            return [f"Ошибка API: {e}"]

    # Для совместимости, если где-то вызывается старое имя
    def get_interfaces(self) -> List[str]:
        return self.get_interface_names()

    def scan_results(self) -> List[str]:
        if not self._manager:
            return ["Ошибка: DLL не найдена"]
        return list(self._manager.ScanNetworks())

    def get_profiles(self) -> List[str]:
        if not self._manager:
            return []
        return list(self._manager.GetProfiles())

    def get_password(self, profile_name: str) -> str:
        if not self._manager:
            return "Ошибка"
        return self._manager.GetProfilePassword(profile_name)

    def get_interface_by_index(self, index: int) -> Optional[str]:
        if 0 <= index < len(self.interfaces):
            return self.interfaces[index]
        return None
