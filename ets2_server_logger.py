import os
import time
import datetime
import discord
from discord import app_commands
import threading
import requests

# --------------------------------------------------------
# Konfiguration
# --------------------------------------------------------
BOT_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Dein Bot-Token
WEBHOOK_URL = "https://discord.com/api/webhooks"  # Webhook-URL für Chat-Log-Embeds (leer lassen = deaktiviert)
GUILD_ID = 1234567890    # Discord-Server-ID
LOG_PATH = r"C:\Users\DEINNAME\Documents\Euro Truck Simulator 2\server.log.txt"


# --------------------------------------------------------
# Discord Bot Grundstruktur
# --------------------------------------------------------
class ETS2Bot(discord.Client):
    def __init__(self, guild_id: int | None):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild_id = guild_id

    async def setup_hook(self):
        if self.guild_id:
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"✅ Slash-Commands für Guild {self.guild_id} synchronisiert.")
        else:
            await self.tree.sync()
            print("✅ Slash-Commands global synchronisiert (kann bis zu 1 Stunde dauern).")


bot = ETS2Bot(GUILD_ID)


# --------------------------------------------------------
# Hilfsfunktionen: Embed Design
# --------------------------------------------------------
def make_embed(title: str, description: str, color=discord.Color.blue()) -> discord.Embed:
    """Einheitliches Embed-Design mit Logo."""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.datetime.now()
    )

    # ✅ Hier dein Logo einfügen (URL zu einem Bild)
    embed.set_thumbnail(url="https://i.imgur.com/5x4tt8L.png")  # <-- Ersetze durch dein Logo

    embed.set_footer(text="🚚 ETS2LS By ISMIREGAL")
    return embed



# --------------------------------------------------------
# Slash-Command: /ets2status
# --------------------------------------------------------
@bot.tree.command(name="ets2status", description="Zeigt an, ob der ETS2-Server aktiv ist.")
async def ets2status(interaction: discord.Interaction):
    if not os.path.exists(LOG_PATH):
        embed = make_embed("❌ ETS2 Server Status", "📁 Die Logdatei wurde nicht gefunden!", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(LOG_PATH))
    diff = datetime.datetime.now() - last_modified
    minutes = int(diff.total_seconds() / 60)

    if diff.total_seconds() < 300:
        embed = make_embed(
            "✅ ETS2 Server Status",
            f"🟢 Der ETS2-Server läuft.\n\n📅 Letzte Aktivität: vor **{minutes} Minuten**",
            discord.Color.green()
        )
    else:
        embed = make_embed(
            "⚠️ ETS2 Server Status",
            f"🟡 Der ETS2-Server ist möglicherweise offline.\n\n📅 Letzte Aktivität: vor **{minutes} Minuten**",
            discord.Color.orange()
        )

    await interaction.response.send_message(embed=embed)


# --------------------------------------------------------
# Slash-Command: /ets2mods
# --------------------------------------------------------
@bot.tree.command(name="ets2mods", description="Zeigt die geladenen ETS2-Mods an.")
async def ets2mods(interaction: discord.Interaction):
    if not os.path.exists(LOG_PATH):
        embed = make_embed("❌ ETS2 Mods", "📁 Die Logdatei wurde nicht gefunden!", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    mods = []
    with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "[mp] mod - " in line.lower():
                mods.append(line.strip())

    if not mods:
        embed = make_embed("📦 ETS2 Mods", "🚫 Keine Mods in der Logdatei gefunden.", discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return

    embed = make_embed("📦 Geladene ETS2 Mods", "Folgende Mods sind aktiv:", discord.Color.purple())
    block = []
    for i, m in enumerate(mods, 1):
        block.append(f"🔹 **{i}.** {m}")
        if len("\n".join(block)) > 950:
            embed.add_field(name="Mods", value="\n".join(block), inline=False)
            block = []
    if block:
        embed.add_field(name="Mods", value="\n".join(block), inline=False)

    embed.set_footer(text=f"📦 Insgesamt {len(mods)} Mods geladen")
    await interaction.response.send_message(embed=embed)


# --------------------------------------------------------
# Slash-Command: /ets2info
# --------------------------------------------------------
@bot.tree.command(name="ets2info", description="Zeigt allgemeine Informationen zum ETS2-Server an.")
async def ets2info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌍 Euro Truck Simulator 2 Server",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )

    embed.add_field(name="🌐 Servername", value="**NetzwerkHQ**", inline=False)
    embed.add_field(name="🗺️ DLCs", value="Alle Map-DLCs erforderlich", inline=False)
    embed.add_field(name="🛠️ Mods", value="Aktiv – aber nur auf Anfrage", inline=False)
    embed.add_field(name="🔑 Passwort", value="Ja", inline=False)

    embed.add_field(
        name="📢 Wichtige Infos",
        value="⚡ Da wir Mods nutzen und der Traffic aktiviert ist, haben wir eine maximale Geschwindigkeit von **90 km/h** eingestellt.\n"
              "👉 **Bitte fahrt anständig und haltet euch an die Regeln – so haben alle mehr Spaß!** 🎉",
        inline=False
    )

    embed.set_footer(text="🚚 ETS2LS By ISMIREGAL")
    await interaction.response.send_message(embed=embed)


# --------------------------------------------------------
# Funktion: Nachricht an Discord senden (per Webhook)
# --------------------------------------------------------
def send_to_discord(message: str):
    """Sendet Chat-Log Nachrichten als Embed an Discord (über Webhook)."""
    if not WEBHOOK_URL:
        return
    try:
        embed = make_embed("💬 ETS2 Chat-Log", message, color=discord.Color.green())
        payload = {"embeds": [embed.to_dict()]}
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code not in (200, 204):
            print(f"⚠️ Fehler beim Webhook Senden {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Fehler beim Senden an Webhook: {e}")


# --------------------------------------------------------
# Logdatei-Überwachung
# --------------------------------------------------------
def tail_log(file_path):
    """Simuliert 'tail -f' und liest neue Zeilen fortlaufend ein."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()


def log_watcher():
    """Überwacht die ETS2-Logdatei und postet Chat-Zeilen in Discord."""
    print("🚚 Starte ETS2 Server-Logger (nur [MP] [Chat]-Zeilen)...")
    print(f"Überwache: {LOG_PATH}")
    for line in tail_log(LOG_PATH):
        if "[mp] [chat]" in line.lower():
            msg = line.strip()
            send_to_discord(msg)
            print(msg)


# --------------------------------------------------------
# Main Start
# --------------------------------------------------------
if __name__ == "__main__":
    # Logdatei-Überwachung im Hintergrund starten
    t = threading.Thread(target=log_watcher, daemon=True)
    t.start()

    # Discord Bot starten
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"Fehler beim Starten des Bots: {e}")
