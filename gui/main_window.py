# gui/main_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from core.wifi_manager import WindowsWifiManager

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("UltimateWiFiAudit v1.0 - Windows 11")
        self.root.geometry("900x650")
        
        # Инициализируем менеджер WiFi
        self.wifi_manager = WindowsWifiManager()
        
        # Стиль
        self.setup_styles()
        
        # Интерфейс
        self.setup_ui()
        
        # Загружаем интерфейсы при старте
        self.load_interfaces()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
    
    def setup_ui(self):
        # Верхняя панель с выбором адаптера
        top_frame = ttk.LabelFrame(self.root, text="Управление адаптерами", padding=10)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(top_frame, text="Выберите WiFi адаптер:").grid(row=0, column=0, padx=5)
        
        self.interface_combo = ttk.Combobox(top_frame, state="readonly", width=50)
        self.interface_combo.grid(row=0, column=1, padx=5)
        
        ttk.Button(top_frame, text="Обновить", command=self.load_interfaces).grid(row=0, column=2, padx=5)
        ttk.Button(top_frame, text="Сканировать сети", command=self.start_scan).grid(row=0, column=3, padx=5)
        ttk.Button(top_frame, text="Показать профили", command=self.show_profiles).grid(row=0, column=4, padx=5)
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Вкладка 1: Сканирование сетей
        scan_frame = ttk.Frame(notebook)
        notebook.add(scan_frame, text="Обнаружение сетей")
        
        # Таблица для сетей (упрощённый вариант)
        self.network_tree = ttk.Treeview(scan_frame, columns=("SSID", "Signal", "Type", "BSSID"), show="headings", height=15)
        self.network_tree.heading("SSID", text="Имя сети (SSID)")
        self.network_tree.heading("Signal", text="Сигнал %")
        self.network_tree.heading("Type", text="Тип")
        self.network_tree.heading("BSSID", text="BSSID")
        
        self.network_tree.column("SSID", width=250)
        self.network_tree.column("Signal", width=80)
        self.network_tree.column("Type", width=100)
        self.network_tree.column("BSSID", width=150)
        
        scrollbar = ttk.Scrollbar(scan_frame, orient="vertical", command=self.network_tree.yview)
        self.network_tree.configure(yscrollcommand=scrollbar.set)
        
        self.network_tree.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        # Вкладка 2: Профили и пароли
        profiles_frame = ttk.Frame(notebook)
        notebook.add(profiles_frame, text="Сохранённые профили")
        
        self.profiles_text = scrolledtext.ScrolledText(profiles_frame, wrap=tk.WORD, width=80, height=20)
        self.profiles_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Нижняя панель с логами
        log_frame = ttk.LabelFrame(self.root, text="Журнал событий", padding=10)
        log_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True)
    
    def load_interfaces(self):
        """Загружает список интерфейсов в комбобокс."""
        interfaces = self.wifi_manager.get_interface_names()
        self.interface_combo['values'] = interfaces
        if interfaces:
            self.interface_combo.current(0)
            self.log(f"[+] Загружено интерфейсов: {len(interfaces)}")
        else:
            self.log("[-] WiFi интерфейсы не обнаружены. Проверьте драйверы.")
    
    def start_scan(self):
        """Запускает сканирование сетей в отдельном потоке."""
        if not self.wifi_manager.interfaces:
            messagebox.showerror("Ошибка", "Нет доступных WiFi интерфейсов!")
            return
        
        # Очищаем предыдущие результаты
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        
        self.log("[~] Начинаю сканирование сетей...")
        
        # Запускаем в отдельном потоке, чтобы не блокировать GUI
        thread = threading.Thread(target=self.perform_scan)
        thread.daemon = True
        thread.start()
    
    def perform_scan(self):
        """Выполняет сканирование сетей."""
        try:
            selected_iface = self.interface_combo.current()
            networks = self.wifi_manager.scan_networks(selected_iface)
            
            # Обновляем GUI из основного потока
            self.root.after(0, self.update_network_table, networks)
            self.root.after(0, self.log, f"[+] Найдено сетей: {len(networks)}")
            
        except Exception as e:
            self.root.after(0, self.log, f"[-] Ошибка сканирования: {e}")
    
    def update_network_table(self, networks):
        """Обновляет таблицу с сетями."""
        for net_str in networks:
            # Парсим строку сети (можно улучшить)
            parts = net_str.split(" | ")
            ssid = parts[0] if len(parts) > 0 else "Unknown"
            signal = parts[1].replace("Сигнал: ", "") if len(parts) > 1 else "0%"
            net_type = parts[2].replace("Тип: ", "") if len(parts) > 2 else "Unknown"
            
            self.network_tree.insert("", "end", values=(ssid, signal, net_type, ""))
    
    def show_profiles(self):
        """Показывает сохранённые профили."""
        if not self.wifi_manager.interfaces:
            messagebox.showerror("Ошибка", "Нет доступных WiFi интерфейсов!")
            return
        
        self.profiles_text.delete(1.0, tk.END)
        selected_iface = self.interface_combo.current()
        
        self.log("[~] Загружаю сохранённые профили...")
        
        profiles = self.wifi_manager.get_saved_profiles(selected_iface)
        
        if profiles:
            self.profiles_text.insert(1.0, "\n".join(profiles))
            self.log(f"[+] Загружено профилей: {len(profiles)}")
        else:
            self.profiles_text.insert(1.0, "Сохранённые профили не найдены.")
            self.log("[-] Профили не найдены.")
    
    def log(self, message):
        """Добавляет сообщение в лог."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()