# 🎵 Lyrics Discord Bot

A Discord bot that fetches song lyrics instantly using the **Genius API**, supporting both slash commands and prefix commands.

---

## ✨ Features

- 🔍 Search lyrics by song title or title + artist
- 🎨 Beautiful embed display with album art
- 📄 Auto-pagination for long lyrics
- ⚡ Supports both `/lyrics` (slash) and `!lyrics` (prefix) commands
- 🌐 Works across multiple servers simultaneously

---

## 📸 Demo

```
/lyrics Shape of You
!lyrics Blinding Lights | The Weeknd
!l Stay
```

---

## 🛠️ Built With

| Library | Purpose |
|---|---|
| [discord.py](https://discordpy.readthedocs.io/) | Discord API wrapper |
| [lyricsgenius](https://lyricsgenius.readthedocs.io/) | Fetch lyrics from Genius |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Manage environment variables |

---

## ⚙️ Installation

### Requirements
- Python 3.10+
- Discord Bot Token
- Genius API Token

### 1. Clone the repository

```bash
git clone https://github.com/dilinhxinh/lyrics-bot.git
cd lyrics-bot
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
DISCORD_TOKEN=your_discord_bot_token_here
GENIUS_TOKEN=your_genius_access_token_here
```


### 4. Get your tokens

**Discord Token:**
1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a New Application → go to the **Bot** tab → copy the Token
3. Under **Privileged Gateway Intents**, enable **Message Content Intent**

**Genius Token:**
1. Sign up at [genius.com/api-clients](https://genius.com/api-clients)
2. Create a New API Client → copy the **Client Access Token**

### 5. Run the bot

```bash
python bot.py
```

---

## 📖 Usage

| Command | Description |
|---|---|
| `/lyrics <song>` | Search lyrics via slash command |
| `/lyrics <song> <artist>` | Search with artist for accurate results |
| `!lyrics <song>` | Search lyrics via prefix command |
| `!lyrics <song> \| <artist>` | Search with artist name |
| `!l <song>` | Shorthand for `!lyrics` |
| `!help` | Show usage guide |

---

## 🗂️ Project Structure

```
lyrics-bot/
├── bot.py           # Entry point, starts the bot
├── cogs/
│   └── lyrics.py    # Lyrics search logic
├── .env             # Secret tokens (never upload this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Deployment (24/7)

Host the bot for free on:
- [Railway.app](https://railway.app) — Easiest, recommended
- [Render.com](https://render.com) — Free tier available
- [Oracle Cloud](https://www.oracle.com/cloud/free/) — Always free

---

## 📝 Notes

- Bot requires `Send Messages`, `Embed Links`, and `Read Message History` permissions
- Slash commands may take a few minutes to sync when joining a new server
- Genius API has rate limits — avoid spamming commands

---

## 📄 License

MIT License — free to use and modify.

---
Author: Dieu Linh Nguyen