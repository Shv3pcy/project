"""BMI calculator handler module for SysBmi_Bot

Contains handlers for BMI calculation functionality.

t.me/SysBmi_Bot
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.calculator import bmi_calc

router = Router()

class BmiStates(StatesGroup):
    """States for BMI calculator"""
    body_weight = State()
    body_height = State()

@router.callback_query(F.data == "bmi_calc")
async def bmi_menu(clb: CallbackQuery, state: FSMContext):
    """Handler for BMI calculator menu button
    
    Starts the BMI calculation process by asking for weight
    """
    await clb.answer()
    await state.set_state(BmiStates.body_weight)
    await clb.message.reply(
        "Введи свою массу тела в килограммах. Принимаем только целые значения.\n<blockquote>Для отмены - /cancel</blockquote>",
        parse_mode="html",
    )

@router.message(BmiStates.body_weight)
async def process_weight(message: Message, state: FSMContext):
    """Handler for weight input
    
    Validates weight input and asks for height
    """
    try:
        await state.update_data(body_weight=message.text)
        data = await state.get_data()

        if int(data["body_weight"]) >= 1000:
            await message.reply("Нельзя вводить значения больше 1000!\nПопробуй заново")
            await state.set_state(BmiStates.body_weight)
        else:
            await state.set_state(BmiStates.body_height)
            await message.reply("Введи свой рост в метрах (например, 177см -> 1.77).")

    except Exception as e:
        await message.reply(
            f"Ошибка! Возможно, ты ввел(а) данные в неправильном формате. Попробуй заново.\n<pre><code class=language-Error>{e}</code></pre>",
            parse_mode="html",
        )
        await state.set_state(BmiStates.body_weight)

@router.message(BmiStates.body_height)
async def process_height(message: Message, state: FSMContext):
    """Handler for height input
    
    Calculates BMI based on weight and height and provides recommendations
    """
    try:
        await state.update_data(body_height=message.text)
        data = await state.get_data()
        body_height = float(data["body_height"])
        body_weight = int(data["body_weight"])

        if body_height >= 10:
            await message.reply(
                f"Ты ввел(а) данные в неправильном формате:\n<blockquote>Значение нужно указать в метрах, и не выше 10</blockquote>",
                parse_mode="html",
            )
        else:
            result = bmi_calc(body_weight, body_height)
            if float(result) < 18:
                await message.reply(
                    f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nТы худоват(а), тебе нужно набрать массу</blockquote>",
                    parse_mode="html",
                )
            elif float(result) >= 18 and float(result) < 25:
                await message.reply(
                    f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nУ тебя средний ИМТ, это хорошо</blockquote>",
                    parse_mode="html",
                )
            else:
                await message.reply(
                    f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nТебе нужно подбросить вес.</blockquote>",
                    parse_mode="html",
                )
            await state.clear()

    except Exception as e:
        await message.reply(
            f"Ошибка! Возможно, ты ввел(а) данные в неправильном формате. Попробуй заново.\n<pre><code class=language-Error>{e}</code></pre>",
            parse_mode="html",
        )
        await state.set_state(BmiStates.body_weight)