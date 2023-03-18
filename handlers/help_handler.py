from telebot import TeleBot


def handle(bot: TeleBot):
    @bot.message_handler(commands=["help"])
    def help(message):
        if message.chat.type != 'private':
            return

        bot.send_message(
            message.chat.id,
            'Если у Вас возникли трудности, свяжитесь со мной напрямую @business_jet.',
        ) 
