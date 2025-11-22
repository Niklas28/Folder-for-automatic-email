import time
import os
import webbrowser
import json
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_FILE = "config.json"

# Funktion, um den gespeicherten Pfad zu laden
def lade_watch_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("watch_path", "")
    return ""

# Funktion, um den Pfad zu speichern
def speichere_watch_path(path):
    # Prüfen, ob die Datei existiert
    if not os.path.exists(CONFIG_FILE):
        print(f"{CONFIG_FILE} existiert nicht. Wird jetzt erstellt.")
    with open(CONFIG_FILE, "w") as f:
        json.dump({"watch_path": path}, f)
    print(f"Pfad gespeichert: {path}")


# Pfad laden
WATCH_PATH = lade_watch_path()

# Falls kein Pfad gesetzt ist, Dialog öffnen
if WATCH_PATH == "" or not os.path.exists(WATCH_PATH):
    root = tk.Tk()
    root.withdraw()  # Versteckt das Hauptfenster
    ordner = filedialog.askdirectory(title="Bitte Zielordner auswählen")
    if ordner:
        WATCH_PATH = ordner
        speichere_watch_path(WATCH_PATH)
    else:
        print("Kein Ordner ausgewählt. Programm beendet.")
        exit(1)

print(f"Überwachter Ordner: {WATCH_PATH}")

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Neue Datei entdeckt: {event.src_path}")
            # Outlook-Compose öffnen
            webbrowser.open("https://outlook.office.com/mail/deeplink/compose")

if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    observer.start()

    print("Beobachte Ordner... (Strg+C zum Stoppen)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
