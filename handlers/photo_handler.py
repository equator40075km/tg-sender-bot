from telebot import TeleBot, types
from handlers.buttons import manage_data
import content
from log import logger


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['photo', 'document'])
    def photo(message: types.Message):
        try:
            file_id = None

            if message.content_type == 'photo':
                file_id = message.photo[-1].file_id
            if message.content_type == 'document' and message.document.mime_type.startswith('image'):
                file_id = message.document.file_id

            if file_id is None:
                return

            if content.count_user_media(message.from_user.username, message.chat.id) >= content.MAX_MEDIA:
                bot.send_message(
                    message.chat.id,
                    f"Сохранено уже {content.MAX_MEDIA} Ваших медиа файлов. Отправьте или удалите их.",
                    reply_markup=manage_data
                )
                return
            
            if message.caption:
                content.save_content(
                    message.from_user.username,
                    message.chat.id,
                    content.TEXT_KEY,
                    message.caption
                )

            content.save_content(
                message.from_user.username,
                message.chat.id,
                content.PHOTO_KEY,
                file_id
            )

            if content.set_media_save_time(message.from_user.username, message.chat.id):
                bot.send_message(
                    message.chat.id,
                    'Ваш контент был успешно сохранен.',
                    reply_markup=manage_data
                )

        except Exception as e:
            logger.exception("Ошибка отправки изображения:\n%s" % e)  
