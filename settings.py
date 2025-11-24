import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.json"

# --- Hilfsfunktionen ---
def config_laden():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def config_speichern(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- GUI-Funktion ---
def settings_gui():
    config = config_laden()

    # Default-Werte
    watch_path = config.get("watch_path", "")
    empfaenger = config.get("empfaenger", "")
    betreff = config.get("betreff", "")
    body = config.get("body", "")

    root = tk.Tk()
    root.title("MailWatcher Einstellungen")
    root.geometry("450x450")

    # ---- LABEL & ENTRY FIELDS ----
    tk.Label(root, text="Empfänger:").pack(anchor="w", padx=10, pady=(10,0))
    entry_empfaenger = tk.Entry(root, width=50)
    entry_empfaenger.pack(padx=10)
    entry_empfaenger.insert(0, empfaenger)

    tk.Label(root, text="Betreff:").pack(anchor="w", padx=10, pady=(10,0))
    entry_betreff = tk.Entry(root, width=50)
    entry_betreff.pack(padx=10)
    entry_betreff.insert(0, betreff)

    tk.Label(root, text="Nachricht (Body):").pack(anchor="w", padx=10, pady=(10,0))
    text_body = tk.Text(root, width=50, height=8)
    text_body.pack(padx=10)
    text_body.insert("1.0", body)
    
    # ---- ORDNER AUSWAHL ----
    frame = tk.Frame(root)
    frame.pack(fill="x", padx=10, pady=10)

    tk.Label(frame, text="Zielordner:").pack(anchor="w")
    
    entry_watch_path = tk.Entry(frame, width=40)
    entry_watch_path.pack(side="left", padx=(0,5))
    entry_watch_path.insert(0, watch_path)

    def ordner_auswaehlen():
        ordner = filedialog.askdirectory(title="Ordner auswählen")
        if ordner:
            entry_watch_path.delete(0, tk.END)
            entry_watch_path.insert(0, ordner)

    tk.Button(frame, text="Ändern", command=ordner_auswaehlen).pack(side="left")

    # ---- SPEICHERN BUTTON ----
    def speichern():
        new_data = {
            "watch_path": entry_watch_path.get(),
            "empfaenger": entry_empfaenger.get(),
            "betreff": entry_betreff.get(),
            "body": text_body.get("1.0", tk.END).strip()
        }

        config_speichern(new_data)
        messagebox.showinfo("Gespeichert", "Einstellungen erfolgreich gespeichert!")
        root.destroy()

    tk.Button(root, text="Speichern", command=speichern, height=2).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    settings_gui()
