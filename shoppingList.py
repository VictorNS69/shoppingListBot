"""Telegram Bot -> Shopping list bot
@author: Victor Nieves Sanchez
@version: 1.0
@python: 3.6.3
"""

import telegram.ext
import logging
from telegram.ext import *
from gtts import gTTS
import os


"""Start."""
def start (bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm VictorNS69's Bot. Enjoy this \"sopping list\" bot.")
    bot.send_message(chat_id=update.message.chat_id, text="/help for more info.")
    print("start.")

"""All commands"""
def help(bot, update):
    commands = "Here is some help for you:\n" \
               "/start - Start.\n" \
               "/add (items) - Add the item.\n" \
               "/delete (items) - Delete the item.\n" \
               "/show - Prints your list.\n" \
               "/deleteall - Delete all the items.\n" \
               "/toaudio - Creates an audio with the items in your list(also delete the list.).\n" \
               "/help - Brief help of the bot."
    bot.send_message(chat_id=update.message.chat_id, text=commands)
    print("Showing help.")

'''Add item'''
def add(bot, update):
    if update.message.chat_id not in list.keys():
        list[update.message.chat_id] = []
    result = update.message.text.split(' ')
    result.remove('/add')
    for i in result:
        if i == '':
            return
        if i in list[update.message.chat_id]:
            bot.send_message(chat_id=update.message.chat_id, text="Already listed.")
            print("Already listed.")
        else:
            list[update.message.chat_id].append(i)
            bot.send_message(chat_id=update.message.chat_id, text="Added correctly.")
            print ("Item added.")
    print (list)

'''The list to audio'''
def toaudio(bot, update):
    try:
        auxString = ''
        for i in list[update.message.chat_id]:
            auxString += i + '\n'
        tts = gTTS(auxString, lang='es') #Default language: Spanish
        name = str(update.message.chat_id) + ".mp3"
        tts.save(name)
        bot.send_audio(chat_id=update.message.chat_id, audio=open(name, 'rb'))
        list[update.message.chat_id].clear()
        os.remove(name)
        print("Audio sended.")
    except Exception:
        bot.send_message(chat_id=update.message.chat_id, text="No items in the list.")
        print("No items, no audio.")

'''Delete the item'''
def delete(bot, update):
    if update.message.chat_id not in list.keys():
        list[update.message.chat_id] = []
    result = update.message.text.split(' ')
    result.remove('/delete')
    for i in result:
        if i in list[update.message.chat_id]:
            list[update.message.chat_id].remove(i)
            bot.send_message(chat_id=update.message.chat_id, text="Item correctly deleted.")
            print("Deleted.")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="This item is not in the list.")
            print ("Item is not in the list.")
    print(list)

def show(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=", ".join(list[update.message.chat_id]))
    print("Showing the list.")

"""Delete all items."""
def deleteall(bot,update):
    if update.message.chat_id not in list.keys():
        list[update.message.chat_id] = []
    else:
        list[update.message.chat_id] = []
        bot.send_message(chat_id=update.message.chat_id, text="All items deleted.")
        print("All deleted.")

"""Unknown commands"""
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
    print ("Unknown command.")

print("BOT ONLINE!")
bot = telegram.Bot(token='') #Get your token from @BotFather
updater = Updater(token='') #Get your token from @BotFather
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater.start_polling()

list = {}

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)

toaudio_handler = CommandHandler('toaudio', toaudio)
dispatcher.add_handler(toaudio_handler)

delete_handler = CommandHandler('delete', delete)
dispatcher.add_handler(delete_handler)

deleteall_handler = CommandHandler('deleteall', deleteall)
dispatcher.add_handler(deleteall_handler)

show_handler = CommandHandler('show', show)
dispatcher.add_handler(show_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
