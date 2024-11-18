import pyautogui
import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(os.path.join('images', 'favicon.ico'))
        self.root.title("Auto Clicker - psz")
        self.root.geometry("380x150")
        self.root.resizable(False, False)
        
        self.is_running = False
        self.interval_value = 500  # Standaard
        self.interval_unit = "ms"
        self.click_type = "Single"
        self.button_type = "Left"
        
        self.setup_ui()
        
        threading.Thread(target=self.setup_keybindings, daemon=True).start()

    def setup_keybindings(self):
        keyboard.add_hotkey('F1', self.start_clicking)
        keyboard.add_hotkey('F6', self.start_clicking)
        
        keyboard.add_hotkey('F2', self.stop_clicking)
        keyboard.add_hotkey('F7', self.stop_clicking)

    def setup_ui(self):
        vcmd = (self.root.register(self.validate_interval), '%d', '%P')
        
        ttk.Label(self.root, text="Value").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.interval_unit_combo = ttk.Combobox(self.root, values=["Min", "Sec", "Ms"], width=10, state="readonly")
        self.interval_unit_combo.current(2)
        self.interval_unit_combo.grid(row=0, column=1, padx=5, pady=5)
        self.interval_unit_combo.bind("<<ComboboxSelected>>", self.on_unit_change)
        
        ttk.Label(self.root, text="Time").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.interval_entry = ttk.Entry(self.root, width=10, justify="center", validate="key", validatecommand=vcmd)
        self.interval_entry.insert(0, str(self.interval_value))  
        self.interval_entry.grid(row=0, column=3, padx=5)

        ttk.Label(self.root, text="Click").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.click_type_combo = ttk.Combobox(self.root, values=["Single", "Double"], width=10, state="readonly")
        self.click_type_combo.current(0)
        self.click_type_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Button").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.button_type_combo = ttk.Combobox(self.root, values=["Left", "Right"], width=10, state="readonly")
        self.button_type_combo.current(0)
        self.button_type_combo.grid(row=1, column=3, padx=5, pady=5)

        self.start_button = ttk.Button(self.root, text="Start F1 or F6", command=self.start_clicking)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        self.stop_button = ttk.Button(self.root, text="Stop F2 or F7", command=self.stop_clicking)
        self.stop_button.grid(row=2, column=2, columnspan=2, pady=10, padx=5, sticky="ew")

    def validate_interval(self, action, value_if_allowed):
        if action == '1':  
            return value_if_allowed.isdigit()
        return True

    def on_unit_change(self, event):
        if self.interval_unit_combo.get() == "Ms":
            self.interval_value = 500  # Minimaal 500 ms
        elif self.interval_unit_combo.get() == "Sec":
            self.interval_value = 1  # Minimaal 1 seconde
        elif self.interval_unit_combo.get() == "Min":
            self.interval_value = 1  # Minimaal 1 minuut
        self.interval_entry.delete(0, 'end')
        self.interval_entry.insert(0, str(self.interval_value))

    def start_clicking(self):
        interval_input = self.interval_entry.get()
        
        if interval_input.isdigit():
            self.interval_value = int(interval_input)
        else:
            return 
        
        self.interval_unit = self.interval_unit_combo.get()

        if self.interval_unit == "Ms" and self.interval_value < 500:
            self.interval_value = 500
        elif self.interval_unit == "Sec" and self.interval_value > 600:
            self.interval_value = 600
        elif self.interval_unit == "Min" and self.interval_value > 60:
            self.interval_value = 60

        self.interval_entry.delete(0, 'end')
        self.interval_entry.insert(0, str(self.interval_value))

        self.click_type = self.click_type_combo.get()
        self.button_type = self.button_type_combo.get()
        self.is_running = True
        
        threading.Thread(target=self.perform_clicks, daemon=True).start()

    def stop_clicking(self):
        self.is_running = False

    def perform_clicks(self):
        if self.interval_unit == "Min":
            total_delay = self.interval_value * 60  # Minuten naar seconden
        elif self.interval_unit == "Sec":
            total_delay = self.interval_value  # In seconden
        else:
            total_delay = self.interval_value / 1000  # Milliseconden naar seconden
        
        while self.is_running:
            if self.click_type == "Single":
                pyautogui.click(button=self.button_type.lower())
            elif self.click_type == "Double":
                pyautogui.doubleClick(button=self.button_type.lower())
            
            time.sleep(total_delay)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 10), padding=5)
    style.configure("TButton", font=("Arial", 10), padding=5)
    style.configure("TEntry", font=("Arial", 10))
    style.configure("TCombobox", font=("Arial", 10))
    
    root.mainloop()
