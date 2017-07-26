from telegram.ext import Updater, MessageHandler, Filters
from uuid import uuid4
import os

updater = Updater(token='YOUR-BOT-TOKEN')
dispatcher = updater.dispatcher

def photo(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    pw_uuid = str(uuid4())
    pw_uuid = pw_uuid.split('-')[4]
    photo_file.download(pw_uuid + ".jpg")
    os.rename(pw_uuid + ".jpg", "/var/www/pw.rdyrda.fr/i/" + pw_uuid + ".jpg")
    bot.send_message(chat_id=update.message.chat_id, text="https://pw.rdyrda.fr/i/" + pw_uuid + ".jpg")

photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)

updater.start_polling()
updater.idle()
