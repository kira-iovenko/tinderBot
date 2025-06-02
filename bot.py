from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def gpt_dialog(update,context):
    text = update.message.text
    answer = await chatgpt.send_question("Give a clear and short answer on the following question: ", text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update,context)
    else:
        await send_text(update, context, "*Hello!*")
        await send_text(update, context, "You wrote " + update.message.text)

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


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token="javcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("7429492146:AAG6i6lftlXJlzSSeZWN0H-O6k-VPfXn7xQ").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
