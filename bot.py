import logging
import os
import random
import sys
import telegram
import cryptocompare
from uuid import uuid4
from typing import Text
from telegram import user, InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, InlineQueryHandler, CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown

#Solicitar TOKEN
TOKEN = os.getenv("TOKEN") # $env:TOKEN="1749144591:AAFGcfvsegYWDudHxJDjPde_jj4NyvCwrs0"
mode = os.getenv("MODE") # $env:MODE="dev"

#Configurar Logging
logging.basicConfig(
    level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

if __name__ == "__main__":
    #Obtenemos informacion de nuestro bot
    my_bot = telegram.Bot(token = TOKEN)
    #print(my_bot.getMe())

#Enlazamos nuestro updater con nuestro bot
updater = Updater(my_bot.token, use_context=True)

if mode == "dev":
    # Acceso Local (desarrollo)
    def run(updater):
        updater.start_polling()
        print("BOT CARGADO")
        updater.idle() #Permite finalizar el bot con Ctrl + C

elif mode == "prod":
    # Acceso HEROKU (producción)
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", 
                            port=PORT, 
                            url_path=TOKEN, 
                            webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
    #updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")

else:
    logger.info("No se especificó el MODE")
    sys.exit()

def start(update, context):
    #print(update)
    keyboard = [
            [InlineKeyboardButton("BTC", callback_data='BTC')],
            [InlineKeyboardButton("ETH", callback_data='ETH')],
            [InlineKeyboardButton("XMR", callback_data='XMR')],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info(f"El usuario {update.message.chat['first_name']}, ha iniciado una conversación")
    name = update.message.chat['first_name']
    update.message.reply_text(f"Hola {name}, yo soy tu bot.", reply_markup=reply_markup)

def random_number(update,context):
    user_id = update.message.chat['id']
    logger.info(f"El usuario {user_id} ha solicitado un número aleatorio.")
    number = random.randint(0,100)
    context.bot.sendMessage(chat_id= user_id, parse_mode="HTML", text= f"<b>Número</b> aleatorio:\n{number}")

e_coins = ['BTC','ETH','XMR']
currencies = ['EUR','GBP','USD']
currenciesSymbol = ['€','£','$']

def getBTCPrice(update, context):
    priceStr = None
    msg = str()
    for coin in e_coins:
        if coin.upper() == context.args[0].upper():
            for i, cur in enumerate(currencies):
                priceDict = str(cryptocompare.get_price(coin, currency=cur).get(coin).get(cur)).replace('.','\.')
                priceStr = f"Precio {coin} \({cur}\): *_{priceDict}{currenciesSymbol[i]}_*\n"
                msg += priceStr
            
            update.message.reply_text(msg, parse_mode='MarkdownV2')

def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

def echo(update, context):
    user_id = update.message.chat['id']
    logger.info(f"El usuario {user_id} ha enviado un mensaje de texto.")
    text = update.message.text
    context.bot.sendMessage(
        chat_id= user_id,
        parse_mode= "MarkdownV2",
        text= f"*Escribiste:*\n_{text}_"
    )

#Creamos un despachador
dp = updater.dispatcher

#Creamos los manejadores
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("random", random_number))
#dp.add_handler(MessageHandler(Filters.text, echo))  
dp.add_handler(CommandHandler("btc", getBTCPrice))
dp.add_handler(CallbackQueryHandler(button))

run(updater)