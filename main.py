# UltimateWiFiAudit_Win11/main.py
import sys
import os
import tkinter as tk
from gui.main_window import MainWindow

def windows_init():
    """Инициализация, специфичная для Windows"""
    # 1. Проверяем, что WifiCore.dll существует (критично!)
    if not os.path.exists("WifiCore.dll"):
        print("[ОШИБКА] Файл WifiCore.dll не найден!")
        print("Сначала выполните компиляцию C# проекта (запустите compile_csharp.bat)")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    # 2. Создаем необходимые рабочие папки (аналогично create_directory())
    directories = ['logs', 'exports', 'sessions']
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    print("[+] Рабочие каталоги проверены")

    # 3. (Опционально) Проверяем права администратора, если нужно для сканирования
    # ...

def main():
    """Главная функция запуска, как в execute.py"""
    # Инициализация ОС
    windows_init()

    # Создаём и запускаем GUI на Tkinter (аналог QtWidgets.QApplication)
    root = tk.Tk()
    app = MainWindow(root)

    # Здесь можно добавить заставку (splash screen), как в execute.py, если хотите
    # ...

    # Запуск основного цикла GUI (аналог app.exec_())
    root.mainloop()

    # По завершению GUI можно выполнить cleanup для Windows, если нужно
    # ...

if __name__ == '__main__':
    main()