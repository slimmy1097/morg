from tortoise import Tortoise, fields, models, run_async
from config import settings, logger

from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest


class Chat(models.Model):
    '''таблица для хранения инфо о чатах'''
    id = fields.IntField(primary_key=True)
    chat_name = fields.CharField(max_length=50)
    about_chat = fields.CharField(max_length=50)

    class Meta:
        table = 'parsed_chats'


class Uses(models.Model):
    '''Таблица для хранения служебных данных'''
    id = fields.IntField(primary_key=True)
    name_env = fields.CharField(max_length=500, unique=True)
    content = fields.CharField(max_length=500, null=True)

    class Meta:
        table = 'uses'


async def init_main():
    await Tortoise.init(
        db_url=f'sqlite://{settings.DB_PATH_M}',
        modules={'models': ['db.db_work']}
    )
    await Tortoise.generate_schemas()   # создание таблицы, если её (их) нет
    logger.info('База данных готова')


async def get_all_chats():
    chats = await Chat.all()
    if chats:
        for chat in chats:
            logger.info(
                f'ID: {chat.id}, Chat Name: {chat.chat_name}, About Chat: {chat.about_chat}')
        return chats  # Возвращаем список объектов, а не генератор
    else:
        return ''


async def get_words_list():
    words_record = await Uses.filter(id=5555).first()
    if words_record and words_record.content:
        unique_words = ', '.join(set(word.strip()
                                 for word in words_record.content.split(',')))
        return unique_words
    return ''


async def update_words_list(words: str):
    already_exists_words: str = await get_words_list()
    if len(already_exists_words) > 0:
        logger.info(
            f'Список слов для поиска сейчас есть: {already_exists_words}')
        words_lst = [word.strip() for word in words.split(',')]
        al_ex_wrds = [word.strip() for word in already_exists_words.split(',')]
        al_ex_wrds.extend(words_lst)
        content = ', '.join(al_ex_wrds)
    else:
        logger.info(f'Список слов для поиска создан {words=}')
        content = words

    await Uses.update_or_create(
        id=5555,
        defaults={"content": content, 'name_env': 'words'}
    )
    logger.info(f'Список слов обновлён {content=}')


async def delete_words_list(words: str):
    already_exists_words: str = await get_words_list()
    if len(already_exists_words) > 0:
        logger.info(
            f'Есть какие-то слова и можно что-то удалить {already_exists_words}')
        w1 = set(word.strip() for word in already_exists_words.split(','))
        w2 = set(word.strip() for word in words.split(','))

        content = ', '.join(w1-w2)

        await Uses.update_or_create(
            id=5555,
            defaults={"content": content, 'name_env': 'words'}
        )
        logger.info(f'Список слов обновлён {content=}')

    else:
        return 'Нет слов для поиска'


async def add_string_in_table(chat_id, chat_name: str, about_chat: str):
    chat, created = await Chat.update_or_create(
        id=chat_id,
        defaults={
            'chat_name': chat_name,
            'about_chat': about_chat
        }
    )
    if created:
        logger.info(
            f'добавляем информацию о {chat_id=} в БД {created=}')
    else:
        logger.info(
            f'обновляем информацию о {chat_id=} в БД')


api_id = settings.API_ID_M       # замените на свой API ID (целое число)
api_hash = settings.API_HASH_M  # замените на свой API HASH (строка)
phone = settings.MOB_NUMBER


session_name = 'SomeAppForSm_session'
words_from_db = ('йога', 'йоге', 'просветление')


# Функция для поиска слов в тексте
def contains_keywords(text, words_for_search):
    words_for_search = words_from_db
    return any(word in text.lower() for word in words_for_search)


async def find_some_groups(words_for_search_in_about):

    words_for_search_in_about = words_from_db
    group_ids = []
    info_extended_groups = []

    async with TelegramClient(session_name, api_id, api_hash) as client:
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                chat_id = dialog.id
                chat_name = dialog.name

                try:
                    full_chat = await client(GetFullChannelRequest(chat_id))
                    about_chat = full_chat.full_chat.about or False
                    if about_chat:
                        cleaned_about = ' '.join(about_chat.split()).strip()
                        if contains_keywords(cleaned_about, words_for_search_in_about):
                            print('Найденные слова в тексте:\n',
                                  cleaned_about, '\n')
                            group_ids.append(chat_id)
                            info_extended_groups.append(
                                (chat_id, chat_name, about_chat))
                except Exception as e:
                    about_chat = f'Ошибка при получении описания: {e}'

    print(group_ids, sep='\n\n')
    print(info_extended_groups, sep='\n\n')
