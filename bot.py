from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from telegram.constants import ParseMode



from gpt import *
from util import *


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande": "Ariana Grande",
        "date_robbie": "Margo Robbie",
        "date_zendaya": "Zendaya",
        "date_gosling": "Ryan Gosling",
        "date_hardy": "Tom Hardy"
    })


async def date_dialog(update, context):
    text = update.message.text
    answer = await chatgpt.add_message(text)
    await send_text(update, context, answer)


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context, "Amazing choice! Ask the woman/guy on a date in 5 messages")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    if dialog.mode == "date":
        await date_dialog(update, context)
    else:
        await send_text(update, context, "*Hello!*")
        await send_text(update, context, "You wrote " + update.message.text)

        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Enter the work type", {
            "start": "Start",
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

chatgpt = ChatGptService(
    token="javcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("7429492146:AAG6i6lftlXJlzSSeZWN0H-O6k-VPfXn7xQ").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
