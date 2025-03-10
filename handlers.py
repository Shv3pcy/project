from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from calculate import bmi_calc, sys10_2, sys2_10
from en_decode import encode, decode
from injections import injections_list
import ast

router = Router()

class Register(StatesGroup):
    body_weight = State()
    body_height = State()
    f2s_t10s = State()
    f10s_t2s = State()

@router.message(CommandStart())
async def start(message: Message):
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
    await message.reply(
        f"<b>» Основное меню</b><blockquote>/start<i> — приветствие от бота с прикрепленными снизу кнопками (меню):\n\n«Калькулятор ИМТ» — функция, которая считает ваш индекс массы тела по специальной формуле\n\n«Калькулятор систем счислений» — перевести число десятичной системы в двоичную и наоборот</i></blockquote>\n\n<b>» Шифрование</b>\n<blockquote><i>/crypto — получить информацию по шифрованию текста.\n/encode — зашифровать текст\n/decode — расшифровать текст</i></blockquote>\n\n» <b>Системные команды</b><blockquote>«<code>айди</code>»<i> — получить свой ID просто написав в чате команду или получить ID другого человека, ответив на его сообщение в группе.</i>\n«<code>чат айди</code>»<i> — получить ID группы, написав эту команду в ней.</i></blockquote>\n\n<b>» Прочее</b><blockquote>/donate<i> — получить ссылку на донат</i>\n<b><a href='https://github.com/Shv3pcy/project.git'>Репозиторий в GitHub</a></b></blockquote>",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        parse_mode="html",
    )

@router.message(Command("donate"))
async def donate(message: Message):
    donate_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="99 RUB", url="https://yoomoney.ru/fundraise/dOeliARtiuQ.231119"),
            ]
        ]
    )
    await message.reply("Ссылка на донат", reply_markup=donate_button)

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Действие было отменено")

@router.callback_query(F.data == "bmi_calc")
async def reply_menu1(clb: CallbackQuery, state: FSMContext):
    await clb.answer()
    await state.set_state(Register.body_weight)
    await clb.message.reply(
        "Введи свою массу тела в килограммах. Принимаем только целые значения.\n<blockquote>Для отмены - /cancel</blockquote>",
        parse_mode="html",
    )

@router.message(Register.body_weight)
async def ref_body_weighta(message: Message, state: FSMContext):
    try:
        await state.update_data(body_weight=message.text)
        data = await state.get_data()

        if int(data["body_weight"]) >= 1000:
            await message.reply("Нельзя вводить значения больше 1000!\nПопробуй заново")
            await state.set_state(Register.body_weight)

        else:
            await state.set_state(Register.body_height)
            await message.reply("Введи свой рост в метрах (например, 177см -> 1.77).")

    except Exception as e:
        await message.reply(
            f"Ошибка! Возможно, ты ввел(а) данные в неправильном формате. Попробуй заново.\n<pre><code class=language-Error>{e}</code></pre>",
            parse_mode="html",
        )
        await state.set_state(Register.body_weight)

@router.message(Register.body_height)
async def ref_rost(message: Message, state: FSMContext):
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

            elif float(result) == 19 or float(result) < 25:
                await message.reply(
                    f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nУ тебя средний ИМТ, это хорошо</blockquote>",
                    parse_mode="html",
                )

            elif float(result) > 26:
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
        await state.set_state(Register.body_weight)

@router.callback_query(F.data == "calc_ofNumSys")
async def reply_menu2(clb: CallbackQuery):
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
async def system2(clb: CallbackQuery, state: FSMContext):
    await state.set_state(Register.f2s_t10s)
    await clb.answer()
    await clb.message.reply("Введи число двоичной системы, для перевода в десятичную")

@router.message(Register.f2s_t10s)
async def sysfrom2_to10(message: Message, state: FSMContext):
    try:
        await state.update_data(f2s_t10s=message.text)
        data = await state.get_data()
        ban_list_numbers = "23456789"
        if any(char in ban_list_numbers for char in str(data["f2s_t10s"])):
            await message.reply(
                "Это число не является двоичной системой. Введи соответствующее значение."
            )
            await state.set_state(Register.f2s_t10s)
            data = str(data["f2s_t10s"])

        else:
            if len(str(data)) > 99:
                await message.reply(
                    "Число слишком длинное. Лимит 99 символов. Отправь число поменьше."
                )
                await state.set_state(Register.f2s_t10s)

            else:
                s2 = str(data["f2s_t10s"])
                result = sys2_10(number=s2)

                await state.clear()
                await message.reply(
                    f"<blockquote expandable><u>{s2}</u>² -> <code>{result}</code></blockquote>",
                    parse_mode="HTML",
                )
    except Exception as e:
        await message.reply(
            f"<pre><code class=language-Error>{e}</code></pre>\nПри переводе систем, вы используете только <bold>целые числа</bold>, и <bold>не превышающие 99 символов</bold>.",
            parse_mode="html",
        )
        await state.set_state(Register.f2s_t10s)

@router.callback_query(F.data == "from10_to2")
async def system2(clb: CallbackQuery, state: FSMContext):
    await state.set_state(Register.f10s_t2s)
    await clb.answer()
    await clb.message.reply("Введи число десятичной системы, для перевода в двоичную")

@router.message(Register.f10s_t2s)
async def sysfrom2_to10(message: Message, state: FSMContext):
    try:
        await state.update_data(f10s_t2s=message.text)
        data = await state.get_data()
        if len(str(data["f10s_t2s"])) > 326:
            await message.reply(
                "Число слишком длинное. Лимит 326 символов. Отправь число поменьше."
            )
            await state.set_state(Register.f10s_t2s)
        else:

            s10 = int(data["f10s_t2s"])
            result = sys10_2(number=s10)
            await state.clear()
            await message.reply(
                f"<blockquote expandable><u>{s10}</u>¹⁰ -> <code>{result[2:]}</code></blockquote>",
                parse_mode="html",
            )
    except Exception as e:
        await message.reply(
            f"<pre><code class=language-Error>{e}</code></pre>\nПри переводе систем, вы используете только <bold>целые числа</bold>, и <bold>не превышающие 326 символов</bold>.",
            parse_mode="html",
        )
        await state.set_state(Register.f10s_t2s)

@router.message(Command("crypto"))
async def info_crypt(message: Message):
    await message.reply(
        f"Вы можете зашифровывать и расшифровывать данные в текстовом формате.\n\nПримеры использования:\n<blockquote><code>/decode 00111001</code> -> расшифровка</blockquote>\n<blockquote><code>/encode Hello world</code> -> зашифровка</blockquote>",
        parse_mode="html",
    )

@router.message(Command("decode"))
async def decode_cmd(message: Message):
    try:
        msg = await message.reply("🔒 Идет процесс расшифровки двоичного кода..")
        await asyncio.sleep(2)
        message = str(message.text)
        message = message.split(" ")
        message.remove(message[0])
        text = " ".join(message)
        decode_text = decode(bin_txt=text)
        await msg.edit_text("🔐 Почти готово...")
        await asyncio.sleep(1)
        await msg.edit_text(
            f"🔓 Текст был расшифрован.\n<blockquote><code>{decode_text}</code></blockquote>",
            parse_mode="html",
        )
    except Exception as e:
        await msg.edit_text(
            f"На этапе расшифровки появилась ошибка..\n\n<code>error: {e}</code>.\n\nВозможно, ты пытался зашифровать текст? Если да, используй /encode",
            parse_mode="html",
        )

@router.message(Command("encode"))
async def decode_cmd(message: Message):
    try:
        msg = await message.reply("🔓 Идет процесс зашифровки текста..")
        await asyncio.sleep(2)
        message = str(message.text)
        message = message.split(" ")
        message.remove(message[0])
        text = " ".join(message)
        decode_text = encode(text)
        await msg.edit_text("🔐 Почти готово...")
        await asyncio.sleep(1)
        await msg.edit_text(
            f"🔒 Текст был зашифрован.\n<pre><code class='language-Binary code'>{decode_text}</code></pre>\n<i>Нажать для копирования</i>",
            parse_mode="html",
        )
    except Exception as e:
        await msg.edit_text(
            f"На этапе зашифровки появилась ошибка..\n<code>error: {e}</code>",
            parse_mode="HTML",
        )

@router.message(F.text.lower() == "чат айди")
async def chat_id(message: Message):
    if message.from_user.id == message.chat.id:
        await message.reply(
            f"Данная команда предназначена для групп, если вы хотите узнать свой ID, напишите `<code>айди</code>`.",
            parse_mode="HTML",
        )
    else:
        await message.reply(
            f"ID этой группы:<blockquote><code>{message.chat.id}</code></blockquote>\n<i>Нажать для копирования</i>",
            parse_mode="HTML",
        )

@router.message(F.text.lower() == "айди")
async def id(message: Message):
    await message.reply(
        f"Ваш ID:<blockquote><code>{message.from_user.id}</code></blockquote>\n<i>Нажать для копирования</i>",
        parse_mode="HTML",
    )

@router.message()
async def calc(message: Message):
    try:
        for i in injections_list:
            if i in message.text:
                await message.reply("«Выражение» содержит инъекцию 💉")
        example = message.text
        result = ast.literal_eval(example)  # используем ast.literal_eval вместо eval
        await message.reply(
            f"<pre><code class='language-Пример'>{example}</code></pre>\n<pre><code class='language-Ответ'>{result}</code></pre>",
            parse_mode="html",
        )
    except Exception as e:
        await message.reply(
            f"Я не понял, чего ты хочешь.\n<pre>Помощь по боту /help</pre>",
            parse_mode="HTML",
        )