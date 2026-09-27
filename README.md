# Telegram Tap Game — Bot + Mini App

این نسخه شامل:
- Telegram Bot
- دکمه 🎮 Play
- Telegram Mini App
- Tap / Coins
- Energy
- Upgrade
- Daily Reward
- Leaderboard
- SQLite

## 1) نصب

```bash
pip install -r requirements.txt
```

## 2) اجرای Mini App

سرور وب را اجرا کنید:

```bash
python app.py
```

باید آدرس عمومی HTTPS داشته باشید، مثلاً:

```text
https://your-domain.com
```

## 3) ساخت Bot

در Telegram وارد `@BotFather` شوید و `/newbot` را اجرا کنید.
توکن BotFather را دریافت کنید.

توکن را داخل فایل کد ننویسید. آن را به صورت متغیر محیطی تنظیم کنید.

### Linux / macOS

```bash
export BOT_TOKEN="توکن_ربات"
export WEB_APP_URL="https://your-domain.com"
python bot.py
```

### Windows PowerShell

```powershell
$env:BOT_TOKEN="توکن_ربات"
$env:WEB_APP_URL="https://your-domain.com"
python bot.py
```

سپس در تلگرام `/start` بزنید و دکمه 🎮 Play را انتخاب کنید.

## نکته امنیتی

Bot Token را در GitHub، اسکرین‌شات، فایل ZIP عمومی یا چت منتشر نکنید.
اگر توکن لو رفت، از BotFather آن را revoke/regenerate کنید.

## نکته فنی

Mini App باید روی HTTPS عمومی اجرا شود. `localhost` برای استفاده عادی داخل تلگرام مناسب نیست.

این پروژه فقط امتیاز داخل بازی دارد و توکن/برداشت مالی واقعی در آن پیاده‌سازی نشده است.
