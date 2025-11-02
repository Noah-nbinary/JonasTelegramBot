from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ApplicationHandlerStop, MessageHandler, filters
from bot_library import bot_jona
from dotenv import load_dotenv
import os, logging, datetime, random

# Load environment variables from .env file
load_dotenv()

# Other environment variables
TOKEN: Final[str] = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final[str] = os.getenv('TELEGRAM_BOT_NAME')

# Creating Jona Bot for their functions
jona_bot = bot_jona()

# Datetime object
date = datetime.datetime.now().date()

# Creating log file
logging.basicConfig(filename='/app/logs',datefmt='',level=logging.INFO)

help_info = '''
Comandos:

ahorros -> Muestra los ahorros actuales
ahorros <numero> -> Modifica los ahorros actuales
info mes -> Muestra tu información general para el mes

help/ayuda -> Muestra esta información
'''

# To be implemented - Allow messages or commands only for approved users
approved_users = ''
async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in approved_users:
        await update.effective_message.reply_text("Hey! You are not authorized to use this Bot!")
        raise ApplicationHandlerStop

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hola!! Dime como puedo ayudarte : )')


async def update_savings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user provided amount in the command
    message_text = update.effective_message.text.strip()
    
    # Remove the command and get the rest
    if message_text.startswith('/updatesavings'):
        args_text = message_text[len('/updatesavings'):].strip()
        
        if args_text:
            try:
                amount = int(args_text)
                if amount < 0:
                    raise ValueError
                jona_bot.change_value(1, value=amount)
                await update.message.reply_text(f"Ahorros actualizados a {jona_bot.total_ahorros} €")
                print(f'/updatesavings requested - Savings updated to {jona_bot.total_ahorros} €')
                response = jona_bot.display_info()
                await update.message.reply_text(response)
            except ValueError:
                print(f'/updatesavings requested - Invalid number: {amount}')
                await update.message.reply_text("Please provide a valid number: /updatesavings 500")
        else:
            print(f'/updatesavings requested - No argument was provided')
            await update.message.reply_text("Usage: /updatesavings <amount>")

async def month_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = jona_bot.display_info()
    await update.message.reply_text(response)

def handle_response(text: str) -> str:

    processed_text = text.lower()
    args = processed_text.split()

    # Friendly responses
    if 'hola' in processed_text:
        if random.randint(1,12) == 8:
            return '🤨'
        return 'Hola! : )\n¿Cómo te puedo ayudar?'

    if 'que tal' in processed_text or 'como estas' in processed_text:
        frio = [10,11,12,1,2,3,4]
        # Migrar todo esto a una libreria aparte para que no ocupe espacio aqui por favor
        ##################################################################################
        frio_responses = ['Bien!! Con mantita, deseando tomarme una sopita 😊',
        'Aquí, con el frío que pide plan tranqui 🥶', 'Con ganas de que salga el sol, la verdad 🌞',
        'Pensando en lo pronto que anochece, qué locura 🌆', 'Haciendome un cafecito calentito 🤤' ]
        calor_responses = ['Con mucho calor!! Pero resistiendo 🫡', 'En modo supervivencia contra este horno 🥵',
        'Aquí, entre el ventilador y el hielo ✌️', '¡Superbién! La primavera me carga las pilas ⚡']
        helpful_responses = ['En que te puedo ayudar?', 'Con que necesitas ayuda?', 'Cuentame, que se te ha roto 🤨',
        'Que te cuentas hoy?']
        if date.month in frio:
            return random.choice(frio_responses) + '\n' + random.choice(helpful_responses)
        else:
            return random.choice(calor_responses) + '\n' + random.choice(helpful_responses)
    if 'cuentame algo' in processed_text:
        responses = ['']
        emoji_list = ['😊','🥶','🫡','✌️','🤤','🥵','🤨','🤧','😵']
        return random.choice(responses) + ' ' + random.choice(emoji_list)

    if 'ahorros' in processed_text:
    
        if len(args) > 2:
            return 'Usage: ahorros <amount>'

        if len(args) == 1:

            return jona_bot.display_info().splitlines()[1]


        try:
            jona_bot.change_value(1, value=args[1])
            return f'Ahorros actualizados a {jona_bot.total_ahorros} €'

        except:
            return 'Usage: ahorros <amount>'


    if 'help' in processed_text or 'ayuda' in processed_text:
        return help_info

    if 'info mes' in processed_text and len(args) == 2:
        return jona_bot.display_info()

    if '.' in processed_text:
        return 'Esta funcionalidad esta en construcción jeje...'
        ...
        # devolver con update.message.text el ultimo comando que se haya ejecutado

    return 'No me entero...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    # If by any means, the variable is not modified, default response is:
    response = 'No response fetched'

    # Log
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Handle message type
    if message_type == 'group':

        if BOT_USERNAME not in text:
            return

        new_text = text.replace(BOT_USERNAME, '').strip()
        response = handle_response(new_text)

    if message_type == 'private':
        response = handle_response(text)

    # Reply
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')


def main():
    print('Starting up bot...')
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('monthinfo',month_info))
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('updatesavings',update_savings))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    app.run_polling(poll_interval=2)

if __name__ == '__main__':
    main()