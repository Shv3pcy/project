"""Crypto handler module for SysBmi_Bot

Contains handlers for text encoding and decoding functionality.

t.me/SysBmi_Bot
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
from bot.utils.encoder import encode, decode

router = Router()

@router.message(Command("crypto"))
async def info_crypt(message: Message):
    """Handler for the /crypto command
    
    Provides information about encoding and decoding functionality
    """
    await message.reply(
        f"Вы можете зашифровывать и расшифровывать данные в текстовом формате.\n\nПримеры использования:\n<blockquote><code>/decode 00111001</code> -> расшифровка</blockquote>\n<blockquote><code>/encode Hello world</code> -> зашифровка</blockquote>",
        parse_mode="html",
    )

@router.message(Command("decode"))
async def decode_cmd(message: Message):
    """Handler for the /decode command
    
    Decodes binary text to UTF-8 string
    """
    try:
        msg = await message.reply("🔒 Идет процесс расшифровки двоичного кода..")
        await asyncio.sleep(2)
        message_text = str(message.text)
        message_parts = message_text.split(" ")
        message_parts.remove(message_parts[0])
        text = " ".join(message_parts)
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
async def encode_cmd(message: Message):
    """Handler for the /encode command
    
    Encodes text to binary format
    """
    try:
        msg = await message.reply("🔓 Идет процесс зашифровки текста..")
        await asyncio.sleep(2)
        message_text = str(message.text)
        message_parts = message_text.split(" ")
        message_parts.remove(message_parts[0])
        text = " ".join(message_parts)
        encoded_text = encode(text)
        await msg.edit_text("🔐 Почти готово...")
        await asyncio.sleep(1)
        await msg.edit_text(
            f"🔒 Текст был зашифрован.\n<pre><code class='language-Binary code'>{encoded_text}</code></pre>\n<i>Нажать для копирования</i>",
            parse_mode="html",
        )
    except Exception as e:
        await msg.edit_text(
            f"На этапе зашифровки появилась ошибка..\n<code>error: {e}</code>",
            parse_mode="HTML",
        )