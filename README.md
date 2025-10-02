# ISMIREGAL

# 🚚 ETS2 Discord Server Logger (Windows)

Ein Discord-Bot für **Euro Truck Simulator 2 Dedicated Server unter Windows**, der Chat-Logs und Server-Informationen direkt in Discord anzeigt.  
Erstellt mit **Python** und **discord.py**.

---

## ✨ Features

- 📡 **Live Chat-Log**  
  Überwacht die `server.log.txt` und sendet `[MP] [Chat]` Nachrichten automatisch in Discord.

- 🟢 **Server Status**  
  Slash-Command `/ets2status` prüft, ob der Server aktiv ist und zeigt die letzte Aktivität an.

- 📦 **Mods Übersicht**  
  Slash-Command `/ets2mods` listet alle geladenen Mods übersichtlich als Embed auf.

- 🎨 **Discord Embeds**  
  Alle Nachrichten erscheinen in schön gestalteten Discord-Embeds mit Logo & Emojis.

---

## ⚙️ Installation (Windows Server)

### 1. Abhängigkeiten installieren
```powershell
pip install discord.py==2.3.2
pip install requests==2.31.0
pip install python-dotenv==1.0.0

```

### 2. Konfiguration
Öffne die Datei **ets2_server_logger.py** und trage dort deine Zugangsdaten direkt ein:

```python
BOT_TOKEN = "DEIN_DISCORD_BOT_TOKEN"
WEBHOOK_URL = "DEIN_DISCORD_WEBHOOK"
GUILD_ID = 123456789012345678
LOG_PATH = r"C:\Users\Administrator\Documents\Euro Truck Simulator 2\server.log.txt"
```

### 3. Bot starten
```powershell
python ets2_server_logger.py
```
---

## 🖥️ Voraussetzungen

- Windows Server mit installiertem **ETS2 Dedicated Server**  
- Python **3.11+**  
- Discord Bot mit aktivierten **Privileged Gateway Intents**  
- Schreibrechte auf die `server.log.txt`  

---

## 📦 requirements.txt

Falls du keine Datei erstellen willst, kannst du diese Abhängigkeiten direkt installieren:

```txt
discord.py==2.3.2
requests==2.31.0
python-dotenv==1.0.0
```

---

## 📜 Lizenz

Dieses Projekt steht unter der **MIT-Lizenz** – frei nutzbar und anpassbar.

---

## 👨‍💻 Autor

Projekt entwickelt von **ISMIREGAL** 🚀  
Discord: [Community beitreten](https://discord.gg/jWzAaRhKE9)
