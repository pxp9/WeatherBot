#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to get weather information for any city.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Weather Bot, retrieve weather information.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import schedule
import time
import logging
import os
import weather_handler
import time_handler
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup , ParseMode

import telegram.constants as tc
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext , ConversationHandler , CallbackQueryHandler




""" STATES OF CONVERSATION """

INPUT_CITY=0
INPUT_COUNTRY=1
SELECT_DEFAULT_CITY=2

""" CONSTANTS FOR IDIOMS """

SPANISH_LANG= 'ES'
ENGLISH_LANG = 'EN'
default_LANG= SPANISH_LANG

"""" VARIABLES FOR WEATHER """
default_city="Cercedilla"
city_selected=""



def weather(update: Update , context: CallbackContext):
    query = update.callback_query
    query.answer()
    information = weather_handler.get_weather(globals()['default_city'])
    query.message.chat.send_action(action=tc.CHATACTION_TYPING)
    query.message.reply_text(information)
    start(update , context)
    
def change_language_to_spanish(update: Update , context: CallbackContext):
    query= update.callback_query
    query.answer()
    globals()['default_LANG']= SPANISH_LANG
    query.message.reply_text("Idioma cambiado a español "+u'🇪🇸🇪🇸🇪🇸')
    start(update , context)

def change_language_to_english(update: Update , context: CallbackContext):
    query= update.callback_query
    query.answer()
    globals()['default_LANG']= ENGLISH_LANG
    query.message.reply_text("Language changed to English "+u'🇺🇸🇺🇸')
    start(update , context)




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    if(default_LANG == ENGLISH_LANG):
        user.bot.send_message(chat_id=update._effective_chat.id,
            text=fr'Hi {user.mention_html()} !'+' This bot 🤖🤖 gives you weather information for any city in the world!\n\n '+'<b>do</b> /help <b>in order to learn how to use it</b>',
            reply_markup= InlineKeyboardMarkup([
                [InlineKeyboardButton(text=u'🏛🏛'+" default_city_weather "+u'🏛🏛' , callback_data="dcw")],
                [InlineKeyboardButton(text= u'🇪🇸🇪🇸🇪🇸'+" change_to_spanish "+u'🇪🇸🇪🇸🇪🇸' , callback_data="ches")] , 
                [InlineKeyboardButton(text=u'🏢🏢'+" weather_for_any_city "+u'🏢🏢' , callback_data="wfac")]
                ]) , 
            parse_mode=ParseMode.HTML
        )
    elif(default_LANG == SPANISH_LANG):
        user.bot.send_message(chat_id=update._effective_chat.id,
            text=fr'Hola {user.mention_html()} !'+u' Este bot 🤖🤖 provee información del tiempo para cualquier ciudad a nivel mundial!\n\n '+'<b>escribe</b> /help <b>para aprender a usarlo</b>',
            reply_markup= InlineKeyboardMarkup([ 
                [InlineKeyboardButton(text=u'🏛🏛'+" tiempo_ciudad_predeterminada "+u'🏛🏛' , callback_data="dcw")] ,
                [InlineKeyboardButton(text=u'🇺🇸🇺🇸🇺🇸'+" cambia_a_inglés "+u'🇺🇸🇺🇸🇺🇸' , callback_data="chen")] ,
                [InlineKeyboardButton(text=u'🏢🏢'+" tiempo_para_cualquier_ciudad "+u'🏢🏢' , callback_data="wfac")]
                ]) , 
            parse_mode=ParseMode.HTML
        )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if(default_LANG == ENGLISH_LANG):
        update.message.reply_text("there are a few avaible commands \n\n/help for display this information.\n\n/start for inicialize the bot."
        )
    elif(default_LANG == SPANISH_LANG):
        update.message.reply_text("Estos son los comandos disponibles \n\n/help para imprimir esta información.\n\n/start para iniciar el bot."
        )
def weather_city_handler_query(update: Update , context: CallbackContext):
    query= update.callback_query
    query.answer()
    if( default_LANG == SPANISH_LANG):
        query.message.reply_text("Escribe el nombre de una ciudad por favor ")
    elif(default_LANG == ENGLISH_LANG):
        query.message.reply_text("Please write city name")

    return INPUT_CITY
    
def weather_city_handler(update: Update , context: CallbackContext):
    if( default_LANG == SPANISH_LANG):
        update.message.reply_text("Escribe el nombre de una ciudad por favor ")
    elif(default_LANG == ENGLISH_LANG):
        update.message.reply_text("Please write city name")

    return INPUT_CITY

def input_city(update: Update , context: CallbackContext):
   
    text  = update.message.text
    if(text != "."):
        globals()['city_selected'] = text
    else:
        globals()['city_selected'] = default_city
    print(globals()['city_selected'] +" "+update.effective_user.full_name +" "+ update.effective_user.username)

    # if(default_LANG == SPANISH_LANG):
    #     update.message.reply_text("Escribe el acrónimo del país por favor ")
    # elif(default_LANG == ENGLISH_LANG):
    #     update.message.reply_text("Write country acronym please ")

    # return INPUT_COUNTRY

    # if you want to try weather with countries comment this 3 lines below and quit the comment for the other lines commented
    update.message.chat.send_action(action=tc.CHATACTION_TYPING)
    info = weather_handler.get_weather(globals()['city_selected'])
    update.message.reply_text(info)
    start(update , context)
    return ConversationHandler.END
    
# def input_country(update: Update , context: CallbackContext):
#     vars=globals()
#     text = update.message.text.upper()
#     if(text != "."):
#         vars['country_selected']= text
#     else:
#         vars['country_selected']= default_country

#     print(vars['country_selected'])
#     update.message.chat.send_action(action=CHATACTION_TYPING)
#     info = get_weather(vars['city_selected'] , vars['country_selected'])
#     update.message.reply_text(info)
#     return ConversationHandler.END
def default_city_handler_query(update: Update , context: CallbackContext):
    query= update.callback_query
    query.answer()
    if( default_LANG == SPANISH_LANG):
        query.message.reply_text("Escribe el nombre de la nueva ciudad predeterminada por favor ")
    elif(default_LANG == ENGLISH_LANG):
        query.message.reply_text("Write the default new city name please ")
    return SELECT_DEFAULT_CITY


def select_default_city(update: Update , context : CallbackContext):
    
    try:
        possible_city = update.message.text
        print(possible_city +" " +update.effective_user.full_name + " "+ update.effective_user.username)
        weather_handler.city_valid(possible_city)

    except:
        update.message.chat.send_action(action=tc.CHATACTION_TYPING)
        if(default_LANG == ENGLISH_LANG):
           update.message.reply_text("ERROR maybe city is not valid try to rewrite it" )
        elif(default_LANG == SPANISH_LANG):
           update.message.reply_text("ERROR puede que la ciudad no sea válida prueba a reescribirla")
        return ConversationHandler.END

    globals()['default_city'] = possible_city
    
    update.message.chat.send_action(action=tc.CHATACTION_TYPING)
    if( default_LANG == SPANISH_LANG):
        update.message.reply_text("Ciudad actualizada exitosamente")
    elif(default_LANG == ENGLISH_LANG):
        update.message.reply_text("City successfully updated ")
    start(update , context)
    return ConversationHandler.END



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'] , use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    #convertation handler in order to make work buttons
    dp.add_handler(ConversationHandler(

        entry_points=[
            CallbackQueryHandler(pattern="dcw" , callback=weather) ,
            CallbackQueryHandler(pattern="ches" , callback=change_language_to_spanish) ,
            CallbackQueryHandler(pattern="chen" , callback=change_language_to_english),
            CallbackQueryHandler(pattern="wfac" , callback=weather_city_handler_query),
            CallbackQueryHandler(pattern="sdc" , callback=default_city_handler_query),
            CommandHandler('weather_city', callback=weather_city_handler)
        ] ,
        states={ 
        INPUT_CITY:[MessageHandler(Filters.text , input_city)] ,
        SELECT_DEFAULT_CITY:[MessageHandler(Filters.text , select_default_city)]
        # INPUT_COUNTRY: [MessageHandler(Filters.text , input_country)]
        },
        fallbacks=[]
    ))


    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
