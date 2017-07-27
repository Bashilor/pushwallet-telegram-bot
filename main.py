from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from uuid import uuid4
from functools import wraps
import os, sys, time

updater = Updater(token='YOUR-BOT-TOKEN')
dispatcher = updater.dispatcher

LIST_OF_ADMINS = [YOUR-CHAT-ID]


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            bot.send_message(chat_id=update.message.chat_id, text="You can't execute this command ! (WRONG_CHAT_ID")
            print("Unauthorized; access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def photo(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    pw_uuid = str(uuid4())
    pw_uuid = pw_uuid.split('-')[4]
    photo_file.download(pw_uuid + ".jpg")
    os.rename(pw_uuid + ".jpg", "/var/www/pw.rdyrda.fr/i/" + pw_uuid + ".jpg")
    bot.send_message(chat_id=update.message.chat_id, text="https://pw.rdyrda.fr/i/" + pw_uuid + ".jpg")


@restricted
def restart(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)

dispatcher.add_handler(CommandHandler('restart', restart))

updater.start_polling()
updater.idle()