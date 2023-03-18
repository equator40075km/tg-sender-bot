from telebot import TeleBot


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message):
        if message.chat.type != 'private':
            return

        bot.send_message(
            message.chat.id,
            'Привет, ' + message.from_user.first_name +
            '!\nОпишите задачу текстом, прикрепите пример в виде фотографии или видеоролика, который поможет решению задачи'
            '\nWrite /help fro help.',
        )
