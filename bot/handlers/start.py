"""Start handler module for SysBmi_Bot

Contains handlers for start, help, and donate commands.

t.me/SysBmi_Bot
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    """Handler for the /start command
    
    Displays the main menu with options for BMI calculator and number systems calculator
    """
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Калькулятор ИМТ", callback_data="bmi_calc"),
                InlineKeyboardButton(text="Калькулятор систем счислений", callback_data="calc_ofNumSys"),
            ],
            [
                InlineKeyboardButton(text="Репозиторий в GitHub", url="https://github.com/Shv3pcy/project.git"),
            ],
        ]
    )
    await message.reply_photo(
        FSInputFile("./assets/start-banner.png"),
        reply_markup=menu,
        caption=f"Привет, Выбери одно из действий.\nОзнакомиться — /help",
        parse_mode="HTML",
    )

@router.message(Command("help"))
async def help(message: Message):
    """Handler for the /help command
    
    Provides information about all available commands and features
    """
    await message.reply(
        f"<b>» Основное меню</b><blockquote>/start<i> — приветствие от бота с прикрепленными снизу кнопками (меню):\n\n«Калькулятор ИМТ» — функция, которая считает ваш индекс массы тела по специальной формуле\n\n«Калькулятор систем счислений» — перевести число десятичной системы в двоичную и наоборот</i></blockquote>\n\n<b>» Шифрование</b>\n<blockquote><i>/crypto — получить информацию по шифрованию текста.\n/encode — зашифровать текст\n/decode — расшифровать текст</i></blockquote>\n\n» <b>Системные команды</b><blockquote>«<code>айди</code>»<i> — получить свой ID просто написав в чате команду или получить ID другого человека, ответив на его сообщение в группе.</i>\n«<code>чат айди</code>»<i> — получить ID группы, написав эту команду в ней.</i></blockquote>\n\n<b>» Прочее</b><blockquote>/donate<i> — получить ссылку на донат</i>\n<b><a href='https://github.com/Shv3pcy/project.git'>Репозиторий в GitHub</a></b></blockquote>",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        parse_mode="html",
    )

@router.message(Command("donate"))
async def donate(message: Message):
    """Handler for the /donate command
    
    Provides a donation link
    """
    donate_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="99 RUB", url="https://yoomoney.ru/fundraise/dOeliARtiuQ.231119"),
            ]
        ]
    )
    await message.reply("Ссылка на донат", reply_markup=donate_button)

@router.message(Command("cancel"))
async def cancel(message: Message, state):
    """Handler for the /cancel command
    
    Cancels the current operation and clears the state
    """
    await state.clear()
    await message.reply("Действие было отменено")