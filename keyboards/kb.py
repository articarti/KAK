from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_ru import LEX, LEXICON_COMMANDS
from aiogram import Bot
from aiogram.types import BotCommand



# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)


# === Main Menu Keyboard===
btnPhoto = KeyboardButton(text=LEX['photo'])
btnAudio = KeyboardButton(text='Аудио')
btnSentence = KeyboardButton(text='Предложение')
btnChain = KeyboardButton(text='Цепочка ассоциаций')
btnAdj = KeyboardButton(text='Два прилагательных')
MainMenu = ReplyKeyboardMarkup(keyboard=[[btnPhoto, btnAudio],
                                         [btnSentence],
                                         [btnChain, btnAdj]],
                                         resize_keyboard=True)


btnStop = KeyboardButton(text='Стоп⏹')
all_kb = ReplyKeyboardMarkup(keyboard=[[btnStop]], resize_keyboard=True)


photo_buttons = [
    [InlineKeyboardButton(text='Учеба', callback_data='photo_study')],
    [InlineKeyboardButton(text='Практика', callback_data='photo_train')]
]
photo_menu = InlineKeyboardMarkup(inline_keyboard=photo_buttons)



audio_buttons = [
    [InlineKeyboardButton(text='Играть', callback_data='audio_play')]
]
audio_menu = InlineKeyboardMarkup(inline_keyboard=audio_buttons)



sent_buttons = [
    [InlineKeyboardButton(text='Учеба', callback_data='sent_study')],
    [InlineKeyboardButton(text='Практика', callback_data='sent_train')]
]
sentence_menu = InlineKeyboardMarkup(inline_keyboard=sent_buttons)



chain_buttons = [
    [InlineKeyboardButton(text='Играть', callback_data='chain_play')],
    [InlineKeyboardButton(text='Найти ассоциации', callback_data='chain_find')]
]
chain_menu = InlineKeyboardMarkup(inline_keyboard=chain_buttons)



adj_buttons = [
    [InlineKeyboardButton(text='Играть', callback_data='adj_play')]
]
adj_menu = InlineKeyboardMarkup(inline_keyboard=adj_buttons)