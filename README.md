# MailWatcher

Ein kleines Python-Projekt, das automatisch neue Dateien in einem Ordner überwacht und beim Erkennen einer neuen Datei ein Browserfenster mit einer neuen Outlook-E-Mail öffnet.

# Funktionsweise

Überwacht einen Ordner (z. B. Scan-Ordner).

Wenn eine neue Datei auftaucht, öffnet sich automatisch Outlook im Browser mit einer neuen E-Mail.

Läuft als Hintergrundprozess und kann beim Windows-Start automatisch gestartet werden.

# 0. Requirements installieren

pip install -r requirements.txt

# 1. EXE-Datei erstellen

Mit PyInstaller kannst du aus der Python-Datei eine ausführbare EXE erstellen:

pyinstaller --noconsole --onefile mailwatcher.py
pyinstaller --noconsole --onefile settings.py

Die fertigen .exe findest du danach im Ordner dist/.

# 2. EXE automatisch beim Windows-Start ausführen

Erstelle eine Verknüpfung der EXE-Datei (mailwatcher.exe).

Kopiere die Verknüpfung in den Autostart-Ordner:

Win+R -> shell:startup

Jetzt startet der Prozess automatisch, wenn der Computer hochfährt, und läuft im Hintergrund.

# 3. Ordner für Überwachung auswählen

Beim ersten Start des Programms fragt es nach dem Ordner, der überwacht werden soll.

Danach wird die Wahl gespeichert, sodass du nicht jedes Mal einen Ordner auswählen musst.

# 4. Settings (Optional)

Wird settings.exe ausgeführt, so kann der Zielordner für die Beobachtung, Zielkontakt, Betreff und Text voreingestellt werden für die Email.
