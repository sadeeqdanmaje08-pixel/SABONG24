import os
import logging
from datetime import datetime, time
import pytz
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
TIMEZONE = pytz.timezone('Asia/Manila')  # PH time for sabong

# Active hours (PHT)
ACTIVE_START = time(8, 0)
ACTIVE_END = time(23, 0)

# Store users
user_data = {}

def is_active_hours():
    return ACTIVE_START <= datetime.now(TIMEZONE).time() <= ACTIVE_END

def now_str():
    return datetime.now(TIMEZONE).strftime("%b %d, %Y • %I:%M %p PHT")

# ---------- MENU ----------
async def main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Today's Fights", callback_data='fights'),
         InlineKeyboardButton("🏆 Live Events", callback_data='live')],
        [InlineKeyboardButton("📊 Results", callback_data='results'),
         InlineKeyboardButton("🎥 Watch Live", callback_data='watch')],
        [InlineKeyboardButton("💬 Join Community", callback_data='community'),
         InlineKeyboardButton("📞 Contact", callback_data='contact')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in user_data:
        user_data[user.id] = {
            'name': user.first_name,
            'username': user.username,
            'joined': now_str()
        }

    text = f"""
🐓 *Welcome to SABONG24!* 🐓

Hello {user.first_name}! You're now connected to the ultimate sabong hub.

*What you get:*
📅 Daily fight schedules
🏆 Live event updates
📊 Real-time results
🎥 Streaming links
💬 Community access

🕐 *Status:* {'🟢 LIVE NOW' if is_active_hours() else '🟡 Opens at 8:00 AM PHT'}

Choose an option below 👇
"""
    await update.message.reply_text(
        text, reply_markup=await main_menu(), parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📖 *SABONG24 Commands*

/start – Main menu
/fights – Today's fight schedule
/live – Ongoing live events
/results – Latest results
/watch – Streaming links
/community – Join our groups
/contact – Support
/help – This menu

💡 Just tap the menu buttons anytime!
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def fights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
📅 *TODAY'S FIGHTS*
_{now_str()}_

🏟️ *Main Event — Araneta Coliseum*
🕐 1:00 PM — 5-Cock Derby
🕐 4:00 PM — Championship Bout

🏟️ *Undercard — San Juan Arena*
🕐 2:30 PM — 3-Cock Derby

📌 Fight cards update every hour.
Tap 🔔 to get notified.
"""
    kb = [[InlineKeyboardButton("🔔 Notify Me", callback_data='notify'),
           InlineKeyboardButton("🎥 Watch", callback_data='watch')],
          [InlineKeyboardButton("⬅️ Back", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "🟢 LIVE NOW" if is_active_hours() else "🟡 Off-air"
    text = f"""
🏆 *LIVE EVENTS*

{status}

🔴 *Araneta Coliseum* — Derby Round 3
👥 12,400 watching

🔴 *San Juan Arena* — Main Event
👥 8,200 watching

⚠️ Streams open 15 minutes before fight time.
"""
    kb = [[InlineKeyboardButton("🎥 Watch Live", callback_data='watch')],
          [InlineKeyboardButton("⬅️ Back", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📊 *LATEST RESULTS*

🥇 *Fight #12* — Red Rooster def. Blue Hawk
⏱️ Round 2 • 4:12

🥇 *Fight #11* — Thunderbird def. Black Mamba
⏱️ Round 1 • 2:45

🥇 *Fight #10* — Golden Eagle def. Silver Fox
⏱️ Round 3 • 6:30

_Updated a few seconds ago._
"""
    kb = [[InlineKeyboardButton("🔄 Refresh", callback_data='results')],
          [InlineKeyboardButton("⬅️ Back", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎥 *WATCH LIVE*

Choose your platform:

▶️ [Stream 1 – HD](https://example.com/stream1)
▶️ [Stream 2 – Backup](https://example.com/stream2)
▶️ [Facebook Live](https://facebook.com/example)
▶️ [YouTube Live](https://youtube.com/example)

📶 Tips: Use Wi-Fi for smoother playback.
"""
    kb = [[InlineKeyboardButton("⬅️ Back", callback_data='menu')]]
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(kb),
        parse_mode='Markdown', disable_web_page_preview=True
    )

async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
💬 *JOIN OUR COMMUNITY*

• [Main Group](https://t.me/yourgroup)
• [Announcements Channel](https://t.me/yourchannel)
• [Facebook Page](https://facebook.com/yourpage)

Stay updated on every fight! 🐓
"""
    kb = [[InlineKeyboardButton("⬅️ Back", callback_data='menu')]]
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(kb),
        parse_mode='Markdown', disable_web_page_preview=True
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📞 *CONTACT SABONG24*

• Support: @your_username
• Email: support@sabong24.com
• Hours: 8:00 AM – 11:00 PM PHT

We reply within minutes! ⚡
"""
    kb = [[InlineKeyboardButton("⬅️ Back", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

# ---------- TEXT HANDLER ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()

    if not is_active_hours():
        await update.message.reply_text(
            "🌙 *SABONG24 is resting.*\n\n"
            "We open again at *8:00 AM PHT*.\n"
            "Use the menu buttons anytime to browse schedules & results.",
            parse_mode='Markdown'
        )
        return

    if any(w in msg for w in ['hi', 'hello', 'hey']):
        reply = "🐓 Welcome to SABONG24! Tap /start to see the menu."
    elif 'fight' in msg or 'schedule' in msg:
        reply = "📅 Check /fights for today's lineup!"
    elif 'live' in msg or 'watch' in msg:
        reply = "🎥 Tap /watch for live stream links."
    elif 'result' in msg:
        reply = "📊 Tap /results for the latest outcomes."
    elif any(w in msg for w in ['price', 'bayad', 'fee']):
        reply = "💰 For fees & registration, contact @your_username."
    else:
        reply = (
            "🐓 I got your message!\n\n"
            "Try /fights, /live, /results, or /watch."
        )
    await update.message.reply_text(reply, parse_mode='Markdown')

# ---------- BUTTONS ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == 'menu':
        await q.edit_message_text(
            "🐓 *SABONG24 MAIN MENU*\nChoose an option 👇",
            reply_markup=await main_menu(), parse_mode='Markdown'
        )
    elif data == 'fights':
        await q.edit_message_text("📅 Use /fights for today's schedule.", parse_mode='Markdown')
    elif data == 'live':
        await q.edit_message_text("🏆 Use /live for ongoing events.", parse_mode='Markdown')
    elif data == 'results':
        await q.edit_message_text("📊 Use /results for latest results.", parse_mode='Markdown')
    elif data == 'watch':
        await q.edit_message_text("🎥 Use /watch for streams.", parse_mode='Markdown')
    elif data == 'community':
        await q.edit_message_text("💬 Use /community to join.", parse_mode='Markdown')
    elif data == 'contact':
        await q.edit_message_text("📞 Use /contact for support.", parse_mode='Markdown')
    elif data == 'notify':
        await q.edit_message_text("🔔 You're subscribed! You'll get fight alerts.", parse_mode='Markdown')

# ---------- ERROR ----------
async def error_handler(update, context):
    logger.warning(f"Update {update} caused error {context.error}")

# ---------- MAIN ----------
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "🏠 Main menu"),
        BotCommand("fights", "📅 Today's fights"),
        BotCommand("live", "🏆 Live events"),
        BotCommand("results", "📊 Latest results"),
        BotCommand("watch", "🎥 Watch streams"),
        BotCommand("community", "💬 Join community"),
        BotCommand("contact", "📞 Contact support"),
        BotCommand("help", "📖 Help"),
    ])

def main():
    app = (Application.builder()
           .token(BOT_TOKEN)
           .post_init(post_init)
           .build())

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("fights", fights))
    app.add_handler(CommandHandler("live", live))
    app.add_handler(CommandHandler("results", results))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("community", community))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_error_handler(error_handler)

    logger.info("🐓 SABONG24 bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
