import time
import os
import webbrowser
import json
import tkinter as tk
from tkinter import filedialog
from urllib.parse import quote
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_FILE = "config.json"

# -------------------------------
# CONFIG LADEN & SPEICHERN
# -------------------------------
def lade_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def speichere_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# -------------------------------
# CONFIG INITIALISIEREN
# -------------------------------
config = lade_config()

WATCH_PATH = config.get("watch_path", "")
EMPFAENGER = config.get("empfaenger", "")
BETREFF = config.get("betreff", "")
BODY = config.get("body", "")
ZUSATZLICHE_INFO = config.get("zusatzliche_info", "")

# Falls Ordner fehlt → Benutzer auswählen lassen
if WATCH_PATH == "" or not os.path.exists(WATCH_PATH):
    root = tk.Tk()
    root.withdraw()
    ordner = filedialog.askdirectory(title="Bitte Zielordner auswählen")

    if not ordner:
        print("Kein Ordner ausgewählt. Programm beendet.")
        exit(1)

    WATCH_PATH = ordner
    config["watch_path"] = WATCH_PATH
    speichere_config(config)

print(f"Überwachter Ordner: {WATCH_PATH}")


# -------------------------------
# OUTLOOK URL GENERIEREN
# -------------------------------
def baue_outlook_url():
    base = "https://outlook.office.com/mail/deeplink/compose?"

    params = []

    if EMPFAENGER.strip() != "":
        params.append("to=" + quote(EMPFAENGER))
    if BETREFF.strip() != "":
        params.append("subject=" + quote(BETREFF))
    if BODY.strip() != "":
        params.append("body=" + quote(BODY))

    if len(params) == 0:
        return "https://outlook.office.com/mail/?path=/mail/action/compose"


    return base + "&".join(params)


# -------------------------------
# DATEI-WATCHER
# -------------------------------
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        print(f"Neue Datei entdeckt: {filepath}")

        # warten bis Datei vollständig gespeichert ist
        last_size = -1
        while True:
            try:
                new_size = os.path.getsize(filepath)
            except:
                new_size = -1

            if new_size == last_size:
                break

            last_size = new_size
            time.sleep(0.3)

        # Outlook öffnen
        url = baue_outlook_url()
        print("Öffne Outlook mit:", url)
        webbrowser.open(url)


# -------------------------------
# START
# -------------------------------
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
