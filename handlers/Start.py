import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from bot.keyboards import main_kb
from bot.States import SendBugState
from bot.notifications import new_bug


async def start_cmd(message: types.Message):
    # await message.delete()
    await message.answer(f"🤖Вас приветствует бот технической поддержки🤖\n"
                         f"\n"
                         f"Для того чтобы сформировать заявку нажмите кнопку ниже.\n\n"
                         f"Так же вы можете узнать статус заявки.\n\n"
                         f"Если есть пожелания или замечания\n"
                         f"Можете обратиться к @FeldwebelWillman\n"
                         f"Или воспользовтаься обратной связью /feedback",
                         reply_markup=main_kb())


async def get_report(message: types.Message):
    await message.delete()
    await SendBugState.send_bug.set()
    msg = await message.answer("Опишите проблему")
    await asyncio.sleep(5)
    await msg.delete()


async def send_report(message: types.Message, state: FSMContext):
    await state.update_data(bug=message.text)
    await state.update_data(from_user=message.from_user.username)
    data = await state.get_data()
    await state.finish()
    await new_bug(data)
    await message.delete()


def main_register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start', 'help'])
    dp.register_message_handler(get_report, commands=['feedback'])
    dp.register_message_handler(send_report, state=SendBugState.send_bug)
