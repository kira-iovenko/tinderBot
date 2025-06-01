from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

async def hello(update, context):
    await send_text(update, context, "*Hello!*")
    await send_text(update, context, "You wrote" + update.message.text)

    await send_photo(update, context, "avatar_main")
    await send_text_buttons(update, context, "Enter the work type", {
        "start" : "Start",
        "stop": "Stop"
    })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Process starting")
    else:
        await send_text(update, context, "Process stopped")



app = ApplicationBuilder().token("7429492146:AAG6i6lftlXJlzSSeZWN0H-O6k-VPfXn7xQ").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
