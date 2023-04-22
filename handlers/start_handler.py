from telebot import TeleBot
from json import load


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message):
        if message.chat.type != 'private':
            return

        with open("messages.json") as file:
            messages = load(file)

        bot.send_message(
            message.chat.id,
            messages['start'].format(message.from_user.first_name)
        )
