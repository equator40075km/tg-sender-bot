from log import logger
from typing import Union, Dict
from time import time


MEDIA_SAVE_TIME = 5.0
MAX_MEDIA = 10
TEXT_KEY = 'text'
PHOTO_KEY = 'photos'
VIDEO_KEY = 'videos'
TIME_KEY = 'time'
data = {}


def get_user_key(username: str, chat_id: int) -> str:
    return f"{username}_{str(chat_id)}"


def init_user_data(user_key: str) -> None:
    if user_key not in data:
        data[user_key] = {
            TEXT_KEY: '',
            PHOTO_KEY: [],
            VIDEO_KEY: [],
            TIME_KEY: 0.0
        }


@logger.catch
def save_content(username: str,
                 chat_id: int,
                 content_type: str,
                 content: str) -> None:
    user_key = get_user_key(username, chat_id)
    init_user_data(user_key)

    if content_type == TEXT_KEY:
        data[user_key][TEXT_KEY] += f"\n\n{content}" if data[user_key]['text'] else f"{content}"
    elif content_type == PHOTO_KEY or content_type == VIDEO_KEY:
        data[user_key][content_type].append(content)
    else:
        logger.critical(f"Unknown content type: {content_type}")


@logger.catch
def get_content(username: str, chat_id: int) -> Union[Dict, None]:
    user_key = get_user_key(username, chat_id)

    if user_key not in data:
        init_user_data(user_key)

    return data[user_key]


@logger.catch
def remove_content(username: str, chat_id: int) -> None:
    data.pop(get_user_key(username, chat_id))


def is_empty_content(username: str, chat_id: int) -> bool:
    user_key = get_user_key(username, chat_id)

    if user_key not in data:
        return True

    if data[user_key]['text'] or \
            len(data[user_key]['photos']) > 0 or \
            len(data[user_key]['videos']) > 0:
        return False

    return True


def count_user_media(username: str, chat_id: int) -> int:
    user_key = get_user_key(username, chat_id)

    if user_key not in data:
        return 0

    return len(data[user_key]['photos']) + len(data[user_key]['videos'])


def set_media_save_time(username: str, chat_id: int) -> bool:
    user_key = get_user_key(username, chat_id)

    if time() - data[user_key][TIME_KEY] < MEDIA_SAVE_TIME:
        return False

    data[user_key][TIME_KEY] = time()
    return True
