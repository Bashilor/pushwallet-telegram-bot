from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from uuid import uuid4
from functools import wraps
import os, sys, time, fnmatch

BOT_TOKEN = "YOUR-BOT-TOKEN"
LIST_OF_ADMINS = [YOUR-CHAT-ID]

WEBSITE_PATH = "/var/www/pw.rdyrda.fr/"
WEBSITE_URL = "https://pw.rdyrda.fr"
PHOTO_FOLDER = "/i/"
PHOTO_EXTENSION = ".jpg"
AUDIO_FOLDER = "/a/"
AUDIO_EXTENSION = ".mp3"


updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            bot.send_message(chat_id=update.message.chat_id, text="You can't execute this command ! (WRONG_CHAT_ID")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def generate_uuid():
    pw_uuid = str(uuid4())
    pw_uuid = pw_uuid.split('-')[4]
    for root, subdirs, files in os.walk(WEBSITE_PATH):
        for file in files:
            if fnmatch.fnmatch(file, pw_uuid + '.*'):
                generate_uuid()
    return pw_uuid


def photo(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    time.sleep(0.5)
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    pw_uuid = generate_uuid()
    photo_file.download(pw_uuid + PHOTO_EXTENSION)
    os.rename(pw_uuid + PHOTO_EXTENSION, WEBSITE_PATH + PHOTO_FOLDER + pw_uuid + PHOTO_EXTENSION)
    bot.send_message(chat_id=update.message.chat_id, text=WEBSITE_URL + PHOTO_FOLDER + pw_uuid + PHOTO_EXTENSION)


def audio(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    time.sleep(0.5)
    voice_file = bot.get_file(update.message.audio.file_id)
    pw_uuid = generate_uuid()
    voice_file.download(pw_uuid + AUDIO_EXTENSION)
    os.rename(pw_uuid + AUDIO_EXTENSION, WEBSITE_PATH + AUDIO_FOLDER + pw_uuid + AUDIO_EXTENSION)
    bot.send_message(chat_id=update.message.chat_id, text=WEBSITE_URL + PHOTO_FOLDER + pw_uuid + AUDIO_EXTENSION)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bot is starting...")


@restricted
def restart(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)

audio_handler = MessageHandler(Filters.audio, audio)
dispatcher.add_handler(audio_handler)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('restart', restart))

updater.start_polling()
updater.idle()

