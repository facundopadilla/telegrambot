#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ejemplo oficial:
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Para terminar la ejecución del bot, apreta CTRL + C
"""

import logging, os, dialogflow

from google.api_core.exceptions import InvalidArgument
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Loggin en consola
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class DialogFlow():

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ['LLAVE']
        self.DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
        self.DIALOGFLOW_LANGUAGE_CODE = os.environ['DIALOGFLOW_LANGUAGE_CODE']
        self.SESSION_ID = os.environ['SESSION_ID']
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)
    
    def sesion(self, texto):
        input_usuario = dialogflow.types.TextInput(text=texto, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        consulta_usuario = dialogflow.types.QueryInput(text=input_usuario)
        try:
            response = self.session_client.detect_intent(session=self.session, query_input=consulta_usuario)
            respuesta = response.query_result.fulfillment_text
            return u'{0}'.format(respuesta)
        except InvalidArgument:
            raise


def echo(update, context):
    global dialogflow_bot
    respuesta = dialogflow_bot.sesion(update.message.text)
    update.message.reply_text(respuesta)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    """Inicializar el bot"""
    updater = Updater("1290965102:AAFVM1JoMCXD6H1B0tmugtuErMYKVSM9AJM", use_context=True)

    # Dispatcher para registrar los handlers
    dp = updater.dispatcher

    # DialogFlow, recibe el mensaje y contesta
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log de errores
    dp.add_error_handler(error)

    # Iniciar bot
    updater.start_polling()

    # No sé para que es pero estaba acá
    updater.idle()


if __name__ == '__main__':
    dialogflow_bot = DialogFlow()
    main()