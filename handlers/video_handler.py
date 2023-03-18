from telebot import TeleBot, types
import content
from log import logger
from handlers.buttons import manage_data


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['video', 'animation'])
    def video(message: types.Message):
        try:
            file_id = None

            if message.content_type == 'video':
                file_id = message.video.file_id
            if message.content_type == 'animation':
                file_id = message.animation.file_id

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
                content.VIDEO_KEY,
                file_id
            )

            if content.set_media_save_time(message.from_user.username, message.chat.id):
                bot.send_message(
                    message.chat.id,
                    'Ваш контент был успешно сохранен.',
                    reply_markup=manage_data
                )

        except Exception as e:
            logger.exception("Ошибка отправки видео: %s" % e)  
