#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from propertySearcher_util import mail_confirmation
import pandas as pd
from pathlib import Path

basepath = Path('.')
TOKEN = "TOKEN"
PROCEED, CHOOSING, RETRY = range(3)

appointments = ""
email = ""
client = ""
project_name = ""
address = ""
predicted_price = -1000

reply_keyboard = [['Yes', 'No'],
                  ['Quit']]
proceed_kb = [['Proceed', 'Quit']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
proceed = ReplyKeyboardMarkup(proceed_kb, one_time_keyboard=True)

def set_data():
    global appointments
    global email
    global client
    global project_name
    global address
    global predicted_price
    
    data = pd.read_csv(basepath/'user_appointment_detail.csv',dtype=str)
    appointments = data['Appointment'].tolist()
    email = data['Email'][0]
    client = data['Client Name'][0]
    project_name = data['Project Name'][0]
    address = data['Address'][0]
    predicted_price = data['Predicted Price'][0]

def get_appt():
    # set query function here
    appt = query_appt()
    return appt

def get_requests():
    # set queuing function here, future
    num = query_requests()
    return num

def set_response(response, appt):
    # set response function here
    send_response(response, appt)

def query_appt():
    return None if not appointments else appointments.pop(0)

def query_requests():
    # sample API
    return 1

def send_response(response, appt):
    # sample API
    print(f'customer said {response} for {appt}')
    
def send_email(input_email, input_name, view_project, 
               view_date, view_addr, view_time, view_price):
    
    print("Email sent to: \n"
          f'input_email={input_email}\n'
          f'input_name={input_name}\n'
          f'view_project={view_project}\n'
          f'view_date={view_date}\n'
          f'view_addr={view_addr}\n'
          f'view_time={view_time}\n'
          f'view_price={view_price}\n')
    
    mail_confirmation(input_email, 
                      input_name, 
                      view_project, 
                      view_date, 
                      view_addr, 
                      view_time, 
                      view_price)


def start(update, context):

    set_data()
    
    num = get_requests()
    context.user_data['num'] = num 
    update.message.reply_text(
        "Hi! My name is Property Bot. You have {} requests ".format(str(num)) +
        "Would you like to view your viewing requests?",
        reply_markup=proceed)

    return PROCEED


def init_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    appt = get_appt()
    
    if appt is not None:
        context.user_data['appt'] = appt
        update.message.reply_text(
            f'Would you be free on {appt}?',
            reply_markup=markup)

        return RETRY
    
    else:
        update.message.reply_text("The viewer has no more free slots." 
                                  " Thanks for using the service.")
        return ConversationHandler.END



def yes_info(update, context):
    text = update.message.text
    del context.user_data['choice']
    
    set_response(text, context.user_data['appt'])

    update.message.reply_text("Your appointment has been confirmed!" 
                              " You shall receive an email shortly."
                              " Thanks for using the service.")
    appt_date, appt_time = context.user_data['appt'].split(',')
    appt_date = appt_date.strip()
    appt_time = appt_time.strip()
    
    send_email(email, client, project_name, 
            appt_date, address, appt_time, predicted_price)

    return ConversationHandler.END

def ask_again(update, context):
    text = update.message.text
    
    set_response(text, context.user_data['appt'] )
    
    appt = get_appt()
    
    if appt is not None:
        context.user_data['appt'] = appt
        update.message.reply_text(
            f'Would you be free on {appt}?',
            reply_markup=markup)

        return RETRY
    
    else:
        update.message.reply_text("The viewer has no more free slots." 
                                  " Thanks for using the service.")
        return ConversationHandler.END


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Thank you for using this service. Bye!")

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""


def main():
    updater = Updater(TOKEN,
                      use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PROCEED: [MessageHandler(Filters.regex('^Proceed$'),
                                      init_choice),
                       MessageHandler(Filters.regex('^Quit$'),
                                      done)
                       ],
            
            CHOOSING: [MessageHandler(Filters.regex('^Yes$'),
                                      yes_info),
                       MessageHandler(Filters.regex('^No$'),
                                      ask_again),
                       MessageHandler(Filters.regex('^Quit$'),
                                      done)
                       ],

            RETRY: [MessageHandler(Filters.regex('^Yes$'),
                                   yes_info),
                    MessageHandler(Filters.regex('^No$'),
                                   ask_again)
                           ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    # log errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()