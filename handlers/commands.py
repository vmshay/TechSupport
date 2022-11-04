import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from bot.keyboards import main_kb, register_kb
from bot.States import SendBugState
from bot.notifications import new_bug
from bot import database, sql


async def start_cmd(message: types.Message):
    # await message.delete()
    db = database.Database()
    if message.chat.type == 'private':
        if not db.sql_fetchone(sql.check_id(message.from_user.id)):
            await message.answer(f"🤖Вас приветствует бот технической поддержки🤖\n"
                                 f"\n"
                                 f"Для доступа к функционалу необходимо зарегистрироваться\n"
                                 f"..", reply_markup=register_kb())
        elif db.sql_fetchone(f'select approved from users where tg_id ={message.from_user.id}') == '0':
            msg = await message.answer("Аккаунт еще не подтвержден")
            await asyncio.sleep(5)
            await msg.delete()
        else:

            await message.answer(f"🤖Вас приветствует бот технической поддержки🤖\n"
                                 f"\n"
                                 f"Для того чтобы сформировать заявку нажмите кнопку ниже.\n\n"
                                 f"Если есть пожелания или замечания\n"
                                 f"Можете обратиться к @FeldwebelWillman\n"
                                 f"Или воспользовтаься обратной связью /feedback",
                                 reply_markup=main_kb())
    else:
        await message.answer(f"Если Вы хотите оставить заявку, "
                             f"напишите лично @TTITTechSuppBot")


async def get_ticket(message: types.Message):
    if message.chat.type == 'private':
        data = message.get_args()
        db = database.Database()
        try:
            client = db.sql_fetchone(
                f"SELECT users.name FROM users inner join tickets on users.tg_id = tickets.client  WHERE tickets.id = {data}")
            contactor = db.sql_fetchone(
                f"SELECT users.name FROM users inner join tickets on users.tg_id = tickets.contactor  WHERE tickets.id = {data}")
            ticket = db.sql_fetchall(
                f"select id, category, cab,problem,category,status, t_new,t_progress,t_increase, t_completed from tickets where id={data}")

            await message.answer(f"ID: {ticket[0]['id']}\n"
                                 f"Статус: {ticket[0]['status']}\n"
                                 f"Заявитель: {client}\n"
                                 f"Проблема: {ticket[0]['problem']}\n"
                                 f"Инициирована: {ticket[0]['t_new']}\n"
                                 f"Взята в работу; {ticket[0]['t_progress']}\n"
                                 f"Исполнитель: {contactor}\n"
                                 f"Передана выше: {ticket[0]['t_increase']}\n"
                                 f"Закрыта: {ticket[0]['t_completed']}\n"
                                 f"")
        except:
            await message.answer("Такого ID нет")
    else:
        await message.answer(f"Если Вы хотите оставить заявку, "
                             f"напишите лично @TTITTechSuppBot")


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
    dp.register_message_handler(get_ticket, commands=['id'])
