"""System handler module for SysBmi_Bot

Contains handlers for system commands like getting user ID and chat ID.

t.me/SysBmi_Bot
"""

from aiogram import Router, F
from aiogram.types import Message
import ast
from bot.utils.security import check_for_injections

router = Router()

@router.message(F.text.lower() == "чат айди")
async def chat_id(message: Message):
    """Handler for the 'чат айди' command
    
    Returns the ID of the current chat
    """
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
async def user_id(message: Message):
    """Handler for the 'айди' command
    
    Returns the ID of the user who sent the message
    """
    await message.reply(
        f"Ваш ID:<blockquote><code>{message.from_user.id}</code></blockquote>\n<i>Нажать для копирования</i>",
        parse_mode="HTML",
    )

@router.message()
async def calculator(message: Message):
    """Handler for mathematical expressions
    
    Attempts to evaluate simple mathematical expressions
    """
    try:
        # Check for potential code injections
        if check_for_injections(message.text):
            await message.reply("«Выражение» содержит инъекцию 💉")
            return
            
        # Try to evaluate as a mathematical expression
        example = message.text
        result = ast.literal_eval(example)  # Using ast.literal_eval instead of eval for safety
        await message.reply(
            f"<pre><code class='language-Пример'>{example}</code></pre>\n<pre><code class='language-Ответ'>{result}</code></pre>",
            parse_mode="html",
        )
    except Exception:
        # If not a valid expression, just ignore
        pass