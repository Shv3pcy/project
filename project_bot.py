from aiogram import Bot, Dispatcher #импортировали все нужные модули из aiogram
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import  State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot 
import asyncio
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from calculate import bmi_calc, sys10_2, sys2_10
from en_decode import encode, decode


"""                                          
   Me: t.me/shv3pcy
   This Bot: @SysBmi_bot                    
"""

class Register(StatesGroup):  # класс, в котором создаем группу регистров
  body_weight = State()       # регистр для массы тела
  body_height = State()       # регистр для роста тела
  f2s_t10s = State()          # регистр для перевода с 2-ичной системы в 10-ичную
  f10s_t2s = State()          # регистр для перевода с 10-ичной системы в 2-ичную

router = Router() # класс, который будет распределяться в обработчике команд Dispatcher()

async def main():
  bot = Bot(token='7637943132:AAH59Dew5tRrpG62RTZrXMs_1kI9hDT48fI') # API-токен для бота
  dp = Dispatcher() # обработчик команд
  dp.include_router(router)
  await dp.start_polling(bot)
  print('BOT ON (ВКЛ)')

@router.message(CommandStart()) #обработчик команды /start
async def start(message: Message):
   
   menu = InlineKeyboardMarkup(
                            inline_keyboard=
                            [
                            [InlineKeyboardButton(text='Калькулятор ИМТ', callback_data='bmi_calc'),
                            InlineKeyboardButton(text='Калькулятор систем счислений', callback_data='calc_ofNumSys')],
                            [InlineKeyboardButton(text='Репозиторий в GitHub', url='https://github.com/Shv3pcy/project.git')]
                            ]
                            )
                    
   await message.reply_photo(photo="https://dc-agency.org/wp-content/uploads/2019/09/0_veNN9p3Zi4gQa-Zc.png",
                          reply_markup=menu,
                          caption=f"Привет. Выбери одно из действий.\n<blockquote expandable>Калькулятор ИМТ</blockquote>\n<blockquote expandable>Калькулятор систем счислений</blockquote>", 
                          parse_mode='HTML') # parse_mode - специальный параметр, для форматирования текста, чтобы задать тексту шрифт
                                          # reply_markup - параметр, с помощью которого прикрепим кнопки к сообщению
   

@router.message(Command('donate'))
async def donate(message: Message):
   donate_button = InlineKeyboardMarkup(
                       inline_keyboard=[
                     [InlineKeyboardButton(text='99 RUB', url='https://yoomoney.ru/fundraise/dOeliARtiuQ.231119')]
                                       ]
                                       )
   await message.reply("Ссылка на донат", reply_markup=donate_button)

@router.message(Command('cancel')) # обработчик команды /cancel
async def cancel(message: Message, state: FSMContext):
   await state.clear() # метод clear() закрывает (отменяет) все регистры
   await message.reply("Действие было отменено")

   
@router.callback_query(F.data == 'bmi_calc') # обработчик callback запроса "bmi_calc"
async def reply_menu1(clb: CallbackQuery, state: FSMContext):
  await clb.answer()
  await state.set_state(Register.body_weight) # создаем регистр массы тела
  await clb.message.reply("Введи свою массу тела в килограммах. Принимаем только целые значения.\n<blockquote>Для отмены - /cancel</blockquote>", parse_mode='html')

@router.message(Register.body_weight) # ловим регистр массы тела
async def ref_body_weighta(message: Message, state: FSMContext):
   try:
      await state.update_data(body_weight=message.text) 
      data = await state.get_data()

      if int(data['body_weight']) >= 1000: 
         await message.reply("Нельзя вводить значения больше 1000!\nПопробуй заново")
         await state.set_state(Register.body_weight) # заново создаем регистр, при случае ошибки

      else:   
         await state.set_state(Register.body_height) # в случае успеха, создаем новый регистр роста тела

         await message.reply("Введи свой рост в метрах (например, 177см -> 1.77).")
 
   except Exception as e:
      await message.reply(f"Ошибка! Возможно, ты ввел(а) данные в неправильном формате. Попробуй заново.\n<pre><code class=language-Error>{e}</code></pre>", parse_mode='html')
      await state.set_state(Register.body_weight)

@router.message(Register.body_height) # ловим регистр роста тела
async def ref_rost(message: Message, state: FSMContext):
   try:   
      await state.update_data(body_height=message.text)
      data = await state.get_data()
      
      body_height = float(data['body_height'])
      body_weight = int(data['body_weight'])

      if body_height >= 10:
         await message.reply(f"Ты ввел(а) данные в неправильном формате:\n<blockquote>Значение нужно указать в метрах, и не выше 10</blockquote>", parse_mode='html')
      
      else:
         result = bmi_calc(body_weight, body_height)
         if float(result) < 18:
            await message.reply(f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nТы худоват(а), тебе нужно набрать массу</blockquote>", parse_mode='html')
         
         elif float(result) == 19 or float(result) < 25:
            await message.reply(f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nУ тебя средний ИМТ, это хорошо</blockquote>", parse_mode='html')

         elif float(result) > 26:
            await message.reply(f"<blockquote expandable><code>Твой вес: {body_weight} кг.\nТвой рост: {body_height} м.\nТвой индекс массы тела (ИМТ): {result}</code>\nТебе нужно подбросить вес.</blockquote>", parse_mode='html')
         await state.clear()

   except Exception as e:
      await message.reply(f"Ошибка! Возможно, ты ввел(а) данные в неправильном формате. Попробуй заново.\n<pre><code class=language-Error>{e}</code></pre>", parse_mode='html')
      await state.set_state(Register.body_weight)


@router.callback_query(F.data == 'calc_ofNumSys') # обработчик callback запроса
async def reply_menu2(clb: CallbackQuery):
   await clb.answer() 
   basics = InlineKeyboardMarkup(
                            inline_keyboard=
                            [
                            [
                            InlineKeyboardButton(text='2 -> 10', callback_data='from2_to10'),
                            InlineKeyboardButton(text='10 -> 2', callback_data='from10_to2')
                            ]
                            ]
                            )
   await clb.message.reply(f"Выбери тип перевода системы\n<blockquote>Из двоичной в десятичную</blockquote>\n<blockquote>Из десятичной в двоичную</blockquote>\nДля отмены - /cancel", reply_markup=basics, parse_mode='html')

@router.callback_query(F.data == 'from2_to10')
async def system2(clb: CallbackQuery, state: FSMContext):
   await state.set_state(Register.f2s_t10s)
   await clb.answer()
   await clb.message.reply('Введи число двоичной системы, для перевода в десятичную')

@router.message(Register.f2s_t10s)
async def sysfrom2_to10(message: Message, state: FSMContext):
   try:
      await state.update_data(f2s_t10s=message.text)
      data = await state.get_data()
      ban_list_numbers = "2" or "3" or "4"or "5" or "6" or "7" or "8" or "9"
      if ban_list_numbers in str(data['f2s_t10s']):
        await message.reply('Это число не является двоичной системой. Введи соответствующее значение.')
        await state.set_state(Register.f2s_t10s)
        data = str(data['f2s_t10s'])
        
         
      else:
         if len(str(data)) > 99:
           await message.reply("Число слишком длинное. Лимит 99 символов. Отправь число поменьше.")
           await state.set_state(Register.f2s_t10s)

         else:
           s2 = str(data['f2s_t10s'])
           result = sys2_10(number=s2)

           await state.clear()
           await message.reply(f"<blockquote expandable><u>{s2}</u>² -> <code>{result}</code></blockquote>", parse_mode='HTML')
   except Exception as e:
      await message.reply(f"<pre><code class=language-Error>{e}</code></pre>\nПри переводе систем, вы используете только <bold>целые числа</bold>, и <bold>не превышающие 10⁹⁹</bold>.", parse_mode='html')
      await state.set_state(Register.f2s_t10s)
      

@router.callback_query(F.data == 'from10_to2') # обработчик callback запроса
async def system2(clb: CallbackQuery, state: FSMContext):
   await state.set_state(Register.f10s_t2s)
   await clb.answer()
   await clb.message.reply('Введи число десятичной системы, для перевода в двоичную')

@router.message(Register.f10s_t2s)
async def sysfrom2_to10(message: Message, state: FSMContext):
   try:
      await state.update_data(f10s_t2s=message.text)
      data = await state.get_data()
      if len(str(data['f10s_t2s'])) > 326:
         await message.reply("Число слишком длинное. Лимит 326 символов. Отправь число поменьше.")
         await state.set_state(Register.f10s_t2s)
      else:
         
         s10 = int(data['f10s_t2s'])
         result = sys10_2(number=s10)
         await state.clear()
         await message.reply(f"<blockquote expandable><u>{s10}</u>¹⁰ -> <code>{result[2:]}</code></blockquote>", parse_mode='html')
   except Exception as e:
      await message.reply(f"<code>error: {e}</code>\n\nВводи только числа. Буквы и прочие символы не переводятся.\nТы не сможешь переводить слишком большие значения.", parse_mode='html')
      await state.set_state(Register.f10s_t2s)

@router.message(Command('crypto'))
async def info_crypt(message: Message):
   await message.reply(f"Вы можете зашифровывать и расшифровывать данные в текстовом формате.\n\nПримеры использования:\n<blockquote><code>/decode 00111001</code> -> расшифровка</blockquote>\n<blockquote><code>/encode Hello world</code> -> зашифровка</blockquote>", parse_mode='html')

@router.message(Command('decode'))
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
      await msg.edit_text(f"🔓 Текст был расшифрован.\n<blockquote><code>{decode_text}</code></blockquote>", parse_mode='html')
   except Exception as e:
      await msg.edit_text(f"На этапе расшифровки появилась ошибка..\n\n<code>error: {e}</code>.\n\nВозможно, ты пытался зашифровать текст? Если да, используй /encode", parse_mode='html')

@router.message(Command('encode'))
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
      await msg.edit_text(f"🔒 Текст был зашифрован.\n<pre><code class='language-Binary code'>{decode_text}</code></pre>\n<i>Нажать для копирования</i>", parse_mode='html')
   except Exception as e:
      await msg.edit_text(f"На этапе зашифровки появилась ошибка..\n<code>error: {e}</code>",parse_mode='HTML')
     
if __name__ == '__main__':
  try:
      asyncio.run(main())
  except KeyboardInterrupt:
      print('BOT OFF (ВЫКЛ)')
