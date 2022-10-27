from ctypes import resize
from gc import callbacks
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.bot import Bot
from telegram.update import Update
from telegram.ext.dispatcher import Dispatcher
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler
)
import os
PORT = int(os.environ.get('PORT', 512))
BOT_TOKEN = '############'

dash_num, generate_url = range(2)

def start(update, context):
    bot = context.bot 
    bot.send_message(
        update.effective_chat.id,
        "Hey there 👋"
    )

    buttons = [[KeyboardButton("/dashboard")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="what do you want?", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize=True))

    return dash_num

def dash_num(update, context):
    bot = context.bot 
    bot.send_message(
        update.effective_chat.id,
        "enter dashboard number"
    )

    return generate_url

def generate_url(update, context):
    bot = context.bot
    context.user_data["dash_num"] = update.message.text
     
    dash_url = 'https://metabase.[].com/dashboard/'+context.user_data["dash_num"]

    bot.send_message(
        update.effective_chat.id,
        "🔗: "+dash_url
    )
    return ConversationHandler.END 

def cancel(update, context):
    return ConversationHandler.END 


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispacher = updater.dispatcher

    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            dash_num: [MessageHandler(filters=None, callback=dash_num)],
            generate_url: [MessageHandler(filters=None, callback=generate_url)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dash_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('dashboard',dash_num)],
        states={
            generate_url: [MessageHandler(filters=None, callback=generate_url)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispacher.add_handler(start_conv_handler)
    dispacher.add_handler(dash_conv_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=BOT_TOKEN)
    updater.bot.setWebhook('https://metabase-url-generator-bot.herokuapp.com/' + BOT_TOKEN)

    updater.idle()


if __name__ == "__main__":
    main()