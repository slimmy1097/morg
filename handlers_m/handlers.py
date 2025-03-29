
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from db.db_work import get_all_chats, get_words_list, update_words_list, delete_words_list

from config import settings, logger


router = Router()


ALLOWED_USERS = settings.ALLOWED_USERS


async def is_allowed_user(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


class Processes(StatesGroup):
    waiting_for_words = State()
    waiting_for_delete_words = State()


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    user_id = message.from_user.id
    if not await is_allowed_user(user_id):
        logger.info(
            f'выбрана команда не администратором {user_id=}\n список админов: {ALLOWED_USERS=}')
        await message.answer('❌ У вас нет прав для выполнения этой команды!')
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='👀 Посмотреть чаты',
                                  callback_data='view_chats')],
            [InlineKeyboardButton(text='📢 Сделать рассылку',
                                  callback_data='send_newsletter')],
            [InlineKeyboardButton(text='➕ Добавить слова',
                                  callback_data='add_words')],
            [InlineKeyboardButton(text='➖ Убрать слова из поиска',
                                  callback_data='delete_words')],
            [InlineKeyboardButton(text='😳 Посмотреть слова для поиска',
                                  callback_data='show_words')],
        ]
    )

    await message.answer('🍩🍩🍩', reply_markup=keyboard)


@router.callback_query()
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'view_chats':
        response_from_db_get_all_chats = await get_all_chats()
        logger.info(
            f'выбрана команда из меню view_chats, получение инфо о чатах')
        logger.info(f'{response_from_db_get_all_chats=}')
        await callback.message.answer(f'📋 Вот список чатов...\n {response_from_db_get_all_chats}')

    elif callback.data == 'send_newsletter':
        await callback.message.answer('📢 Запущена рассылка...')

    elif callback.data == 'show_words':
        words = await get_words_list()
        await callback.message.answer(f'📢 Слова для поиска по чатам\n {words}')

    elif callback.data == 'add_words':
        await callback.message.answer('➕ Введите слова для добавления через ", "')
        await state.set_state(Processes.waiting_for_words)
        # await state.clear()

    elif callback.data == 'delete_words':
        await callback.message.answer('➕ Введите слова для удаления через ", "\n отмена /cancel')
        await state.set_state(Processes.waiting_for_delete_words)

    await callback.answer()


@router.message(Processes.waiting_for_words, F.text)
async def process_added_words(message: Message, state: FSMContext):
    await update_words_list(message.text)
    await message.answer(f'✅ Добавлены слова')
    await state.clear()


@router.message(Processes.waiting_for_delete_words, Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer('Отмена ввода')
    await state.clear()


@router.message(Processes.waiting_for_delete_words, F.text)
async def process_added_words(message: Message, state: FSMContext):
    await delete_words_list(message.text)
    await message.answer(f'✅ Удалены слова')
    await state.clear()


@router.message(StateFilter(default_state), F.text)
async def process_added_words(message: Message, state: FSMContext):
    await delete_words_list(message.text)
    await message.answer(f'Если нужно меню: /menu')
    await state.clear()
