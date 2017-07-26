from telegram.ext import Updater, MessageHandler, Filters
from uuid import uuid4
import os

updater = Updater(token='YOUR-BOT-TOKEN')
dispatcher = updater.dispatcher

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Did you just send me a photo ?!")
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    pw_uuid = str(uuid4())
    pw_uuid = pw_uuid.split('-')[4]
    photo_file.download(pw_uuid + ".jpg")
    bot.send_message(chat_id=update.message.chat_id, text="Just saved your photo !")
    os.rename(pw_uuid + ".jpg", "/var/www/pw.rdyrda.fr/" + pw_uuid + ".jpg")
    bot.send_message(chat_id=update.message.chat_id, text="https://pw.rdyrda.fr/" + pw_uuid + ".jpg")

echo_handler = MessageHandler(Filters.photo, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
