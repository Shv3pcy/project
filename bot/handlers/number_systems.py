"""Number systems calculator handler module for SysBmi_Bot

Contains handlers for number system conversion functionality.

t.me/SysBmi_Bot
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.calculator import sys2_10, sys10_2
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

class NumberSystemStates(StatesGroup):
    """States for number system calculator"""
    binary_to_decimal = State()
    decimal_to_binary = State()

@router.callback_query(F.data == "calc_ofNumSys")
async def number_systems_menu(clb: CallbackQuery):
    """Handler for number systems calculator menu button
    
    Displays options for conversion between binary and decimal
    """
    await clb.answer()
    basics = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="2 -> 10", callback_data="from2_to10"),
                InlineKeyboardButton(text="10 -> 2", callback_data="from10_to2"),
            ]
        ]
    )
    await clb.message.reply(
        f"Выбери тип перевода системы\n<blockquote>Из двоичной в десятичную</blockquote>\n<blockquote>Из десятичной в двоичную</blockquote>\nДля отмены - /cancel",
        reply_markup=basics,
        parse_mode="html",
    )

@router.callback_query(F.data == "from2_to10")
async def binary_to_decimal_start(clb: CallbackQuery, state: FSMContext):
    """Handler for binary to decimal conversion start
    
    Asks user to input a binary number
    """
    await state.set_state(NumberSystemStates.binary_to_decimal)
    await clb.answer()
    await clb.message.reply("Введи число двоичной системы, для перевода в десятичную")

@router.message(NumberSystemStates.binary_to_decimal)
async def binary_to_decimal_process(message: Message, state: FSMContext):
    """Handler for binary to decimal conversion process
    
    Converts binary input to decimal and displays result
    """
    try:
        await state.update_data(binary_input=message.text)
        data = await state.get_data()
        binary_input = data["binary_input"]
        
        # Validate binary input
        ban_list_numbers = "23456789"
        if any(char in ban_list_numbers for char in binary_input):
            await message.reply(
                "Это число не является двоичной системой. Введи соответствующее значение."
            )
            await state.set_state(NumberSystemStates.binary_to_decimal)
            return

        if len(binary_input) > 99:
            await message.reply(
                "Число слишком длинное. Лимит 99 символов. Отправь число поменьше."
            )
            await state.set_state(NumberSystemStates.binary_to_decimal)
            return

        # Convert and display result
        result = sys2_10(number=binary_input)
        await state.clear()
        await message.reply(
            f"<blockquote expandable><u>{binary_input}</u>² -> <code>{result}</code></blockquote>",
            parse_mode="HTML",
        )
    except Exception as e:
        await message.reply(
            f"<pre><code class=language-Error>{e}</code></pre>\nПри переводе систем, вы используете только <bold>целые числа</bold>, и <bold>не превышающие 99 символов</bold>.",
            parse_mode="html",
        )
        await state.set_state(NumberSystemStates.binary_to_decimal)

@router.callback_query(F.data == "from10_to2")
async def decimal_to_binary_start(clb: CallbackQuery, state: FSMContext):
    """Handler for decimal to binary conversion start
    
    Asks user to input a decimal number
    """
    await state.set_state(NumberSystemStates.decimal_to_binary)
    await clb.answer()
    await clb.message.reply("Введи число десятичной системы, для перевода в двоичную")

@router.message(NumberSystemStates.decimal_to_binary)
async def decimal_to_binary_process(message: Message, state: FSMContext):
    """Handler for decimal to binary conversion process
    
    Converts decimal input to binary and displays result
    """
    try:
        await state.update_data(decimal_input=message.text)
        data = await state.get_data()
        decimal_input = data["decimal_input"]
        
        # Validate decimal input
        if len(decimal_input) > 326:
            await message.reply(
                "Число слишком длинное. Лимит 326 символов. Отправь число поменьше."
            )
            await state.set_state(NumberSystemStates.decimal_to_binary)
            return

        # Convert and display result
        decimal_value = int(decimal_input)
        result = sys10_2(number=decimal_value)
        await state.clear()
        await message.reply(
            f"<blockquote expandable><u>{decimal_value}</u>¹⁰ -> <code>{result[2:]}</code></blockquote>",
            parse_mode="html",
        )
    except Exception as e:
        await message.reply(
            f"<pre><code class=language-Error>{e}</code></pre>\nПри переводе систем, вы используете только <bold>целые числа</bold>, и <bold>не превышающие 326 символов</bold>.",
            parse_mode="html",
        )
        await state.set_state(NumberSystemStates.decimal_to_binary)
