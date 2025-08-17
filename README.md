# Asterisk + Telegram Callbot (Cloud Shell Ready)

## 🚀 Setup Steps
1. Upload this folder to Google Cloud Shell.
2. Run installation:
   ```bash
   bash install.sh
   ```
3. Copy configs into place:
   ```bash
   sudo cp asterisk/pjsip.conf /etc/asterisk/pjsip.conf
   sudo cp asterisk/extensions.conf /etc/asterisk/extensions.conf
   sudo systemctl restart asterisk
   ```
4. Start Telegram bot:
   ```bash
   cd bot
   python3 bot.py
   ```

## 📞 Usage
- In Telegram, send `/call <number>` → initiates call through VoIP.ms trunk.
- Caller hears IVR, enters up to **5 digits ending with #**.
- Send `/results` → see last digits entered.

## ⚙️ Edit Credentials
- **VoIP.ms**: `/etc/asterisk/pjsip.conf`
  - Username: `146025_kali`
  - Password: `Spammingteam100.`
  - Server: `dallas1.voip.ms`
- **Telegram**: `bot/bot.py`
  - Token: embedded, replace if needed.

