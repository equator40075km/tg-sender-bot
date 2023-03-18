import os
from telebot import TeleBot, types
import handlers.buttons as buttons
import content
from log import logger


ACTION_SEND = 'отправить'
ACTION_DELETE = 'удалить'


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['text'])
    def text(message: types.Message):
        if message.text == 'Отправить данные':
            bot.send_message(
                message.chat.id,
                get_confirm_msg(message, ACTION_SEND),
                reply_markup=buttons.confirm_send
            )
            return

        if message.text == 'Удалить данные':
            bot.send_message(
                message.chat.id,
                get_confirm_msg(message, ACTION_DELETE),
                reply_markup=buttons.confirm_remove
            )
            return

        if message.text == 'Отправить ✅':
            send_user_data(bot, message)
            return

        if message.text == 'Удалить ❌':
            delete_user_data(bot, message)
            return

        if message.text == 'Отмена 🚫':
            bot.send_message(
                message.chat.id,
                'Действие отменено',
                reply_markup=buttons.manage_data
            )
            return

        try:
            content.save_content(
                message.from_user.username,
                message.chat.id,
                content.TEXT_KEY,
                message.text
            )
            bot.send_message(
                message.chat.id,
                'Ваш текст успешно был записан',
                reply_markup=buttons.manage_data
            )
        except Exception as e:
            logger.exception("Ошибка отправки сообщения: %s" % e)


def send_user_data(bot: TeleBot, message: types.Message):
    if content.is_empty_content(message.chat.username, message.chat.id):
        bot.send_message(message.chat.id, "Для Вас нет сохраненных данных.")
        return

    data = content.get_content(
        message.chat.username,
        message.chat.id
    )

    text = f"Данные от @{message.chat.username}"
    if data[content.TEXT_KEY] is not None:
        text += '\n\n' + data[content.TEXT_KEY]

    caption_added = False
    media_group = []
    for file_id in data[content.PHOTO_KEY]:
        if not caption_added:
            caption_added = True
            media_group.append(types.InputMediaPhoto(file_id, caption=text))
        else:
            media_group.append(types.InputMediaPhoto(file_id))

    for file_id in data[content.VIDEO_KEY]:
        if not caption_added:
            caption_added = True
            media_group.append(types.InputMediaVideo(file_id, caption=text))
        else:
            media_group.append(types.InputMediaVideo(file_id))

    try:
        if len(media_group) > 0:
            bot.send_media_group(os.getenv('TO_CHAT_ID'), media_group)
        else:
            bot.send_message(os.getenv('TO_CHAT_ID'), text)
    except Exception as e:
        logger.exception(f"Send media error:\n{e}")

    content.remove_content(
        message.chat.username,
        message.chat.id
    )

    bot.send_message(
        message.chat.id,
        "Все Ваши данные были пересланы и удалены.",
        reply_markup=buttons.remove_markup
    )


def delete_user_data(bot: TeleBot, message: types.Message):
    if content.is_empty_content(message.chat.username, message.chat.id):
        bot.send_message(message.chat.id, "Для Вас нет сохраненных данных.")
        return

    content.remove_content(
        message.chat.username,
        message.chat.id
    )
    bot.send_message(
        message.chat.id,
        "Все Ваши данные были удалены.",
        reply_markup=buttons.remove_markup
    )


def get_confirm_msg(message: types.Message, action: str) -> str:
    user_data = content.get_content(message.chat.username, message.chat.id)

    result = 'У вас сохранено:\n'
    if user_data[content.TEXT_KEY]:
        result += '\t\tтекст,\n'
    result += f"\t\tизображения - {len(user_data[content.PHOTO_KEY])},\n" \
              f"\t\tвидео - {len(user_data[content.VIDEO_KEY])}.\n" \
              f"Вы действительно хотите {action} данные?"
    if action == ACTION_SEND:
        result += ' После этого все данные будут удалены.'

    return result
