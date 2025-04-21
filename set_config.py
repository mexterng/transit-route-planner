import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import configparser
from utils.config_loader import load_config_ini, Config  # Angepasster Import
from tkcalendar import DateEntry
from datetime import datetime, timedelta

CONFIG_PATH = Path("config.ini")

class ConfigEditor(tk.Tk):
    def __init__(self, config_path: Path):
        super().__init__()
        self.title("Config Editor")
        self.resizable(False, False)
        self.config_path = config_path
        self.config_data: Config = load_config_ini(str(config_path))
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.grid(padx=10, pady=10, sticky="nsew")

        # Frame für Datum und Uhrzeit
        date_time_frame = ttk.Frame(frame)
        date_time_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)

        # Datumsauswahl
        min_date = datetime.now().date() - timedelta(days=6)
        max_date = datetime.now().date() + timedelta(days=99)
        ttk.Label(date_time_frame, text="Datum:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        dt_obj = datetime.strptime(self.config_data.datetime, "%Y-%m-%dT%H:%M:%S")
        self.date_entry = DateEntry(date_time_frame, width=12, background='darkblue', foreground='white', borderwidth=2, 
                                    date_pattern='dd.mm.yyyy', locale='de_DE', mindate=min_date, maxdate=max_date)
        self.date_entry.set_date(dt_obj.date())
        self.date_entry.grid(row=0, column=1, sticky="w", padx=(0, 10))

        # Uhrzeit Auswahl (Dropdowns für Stunde und Minute)
        ttk.Label(date_time_frame, text="Uhrzeit:").grid(row=0, column=2, sticky="w", padx=(0, 5))

        # Stunde
        self.hour_cb = ttk.Combobox(date_time_frame, width=3, values=[f"{h:02}" for h in range(24)], state="readonly")
        self.hour_cb.set(dt_obj.strftime("%H"))
        self.hour_cb.grid(row=0, column=3, sticky="w", padx=(0, 5))

        ttk.Label(date_time_frame, text=":").grid(row=0, column=4, sticky="w", padx=(0, 5))

        # Minute
        self.minute_cb = ttk.Combobox(date_time_frame, width=3, values=[f"{m:02}" for m in range(0, 60, 5)], state="readonly")
        self.minute_cb.set(f"{(dt_obj.minute // 5) * 5:02}")
        self.minute_cb.grid(row=0, column=5, sticky="w", padx=(0, 10))

        # CSV: Schüler
        self.create_file_picker(frame, "Schüleradressen (.csv)", "students_csv", self.config_data.students_csv, 1)

        # CSV: Schulen
        self.create_file_picker(frame, "Schuladressen (.csv)", "schools_csv", self.config_data.schools_csv, 2)

        # Ausgabeordner
        ttk.Label(frame, text="Ausgabeordner:").grid(row=3, column=0, sticky="w", pady=5)
        folder_entry = ttk.Entry(frame, width=40)
        folder_entry.insert(0, self.config_data.output_path)
        folder_entry.grid(row=3, column=1, padx=5, sticky='w')
        self.entries["output_path"] = folder_entry
        folder_btn = ttk.Button(frame, text="Ordner wählen", command=lambda: self.pick_folder("output_path"))
        folder_btn.grid(row=3, column=2, sticky='w')

        # API Key
        ttk.Label(frame, text="API Key:").grid(row=4, column=0, sticky="w", pady=5)
        api_entry = ttk.Entry(frame, width=40)
        api_entry.insert(0, self.config_data.api_key)
        api_entry.grid(row=4, column=1, padx=5, sticky='w')
        self.entries["api_key"] = api_entry

        # Speicher- und Abbrechen-Button
        btn_frame = ttk.Frame(self)
        btn_frame.grid(pady=10, padx=10, sticky="ew", row=5, column=0)

        # Speicher-Button
        save_btn = ttk.Button(btn_frame, text="Speichern", command=self.save_config)
        save_btn.grid(row=0, column=0, padx=5, sticky="e")

        # Abbrechen-Button
        cancel_btn = ttk.Button(btn_frame, text="Abbrechen", command=self.quit)
        cancel_btn.grid(row=0, column=1, padx=5, sticky="w")

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

    def create_file_picker(self, frame, label, key, value, row):
        ttk.Label(frame, text=f"{label}:").grid(row=row, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=40)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=5, sticky='w')
        self.entries[key] = entry
        btn = ttk.Button(frame, text="Datei wählen", command=lambda: self.pick_file(key, label))
        btn.grid(row=row, column=2, sticky='w')

    def pick_file(self, key, label):
        path = filedialog.askopenfilename(filetypes=[(label, "*.csv")])
        if path:
            relative_path = self.get_relative_path(path)
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, relative_path)

    def pick_folder(self, key):
        path = filedialog.askdirectory()
        if path:
            relative_path = self.get_relative_path(path)
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, relative_path)

    def get_relative_path(self, full_path):
        full_path = Path(full_path)
        SCRIPT_DIR = Path(__file__).resolve().parent
        if SCRIPT_DIR in full_path.parents:
            relative_path = full_path.relative_to(SCRIPT_DIR)
            return str(relative_path)
        else:
            return full_path.as_posix()

    def save_config(self):
        hour = self.hour_cb.get()
        minute = self.minute_cb.get()

        if not hour or not minute:
            messagebox.showerror("Fehler", "Bitte Stunde und Minute auswählen.")
            return

        time_obj = datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
        dt_combined = datetime.combine(self.date_entry.get_date(), time_obj)
        datetime_str = dt_combined.strftime('%Y-%m-%dT%H:%M:%S')

        parser = configparser.ConfigParser()
        parser['GENERAL'] = {
            'datetime': datetime_str
        }
        parser['FILES'] = {
            'students_csv': Path(self.entries['students_csv'].get()).as_posix(),
            'schools_csv': Path(self.entries['schools_csv'].get()).as_posix(),
            'output_folder': Path(self.entries['output_path'].get()).as_posix()
        }
        parser['API'] = {
            'api_key': self.entries['api_key'].get()
        }

        with open(self.config_path, 'w') as configfile:
            parser.write(configfile)

        messagebox.showinfo("Erfolg", "Konfigurationsdatei config.ini wurde gespeichert.")
        self.quit()

if __name__ == "__main__":
    app = ConfigEditor(CONFIG_PATH)
    app.mainloop()