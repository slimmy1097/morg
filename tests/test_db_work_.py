import pytest
import pytest_asyncio
from tortoise import Tortoise
from db.db_work import init_main, add_string_in_table, get_all_chats
from db.db_work import Chat  # Импорт модели


# тестовая БД (sqlite в памяти)
TEST_DB_URL = 'sqlite://:memory:'


@pytest_asyncio.fixture(scope='function', autouse=True)
async def init_test_db():
    '''Фикстура для инициализации тестовой базы перед каждым тестом'''
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={'models': ['db.db_work']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()  # Закрываем соединение после тестов


@pytest.mark.asyncio
async def test_add_string_in_table():
    '''Добавить новый чат в базу данных.'''
    await add_string_in_table(12344, 'Test_name_1', 'description 111')

    chat = await Chat.filter(id=12344).first()
    assert chat is not None
    assert chat.chat_name == 'Test_name_1'
    assert chat.about_chat == 'description 111'


@pytest.mark.asyncio
async def test_get_all_chats():
    '''Проверка списка чатов в базе данных'''
    await add_string_in_table(12344, 'Test_name_1', 'description 111')
    await add_string_in_table(22222, 'Test_name_2', 'description 222')
    await add_string_in_table(33333, 'Test_name_3', 'description 333')

    info_all_chats = await get_all_chats()

    assert info_all_chats is not None
    assert len(info_all_chats) == 3  # Ожидаем 3 добавленных чата
