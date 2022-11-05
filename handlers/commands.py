import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from bot.keyboards import main_kb, register_kb
from bot.States import SendBugState
from bot.notifications import new_bug
from bot import database, sql
from datetime import datetime
from bot import config as cnf


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
        admins = cnf.ADMINS.split(" ")
        data = message.get_args()
        db = database.Database()
        if str(message.from_user.id) not in admins:
            await message.answer("Доступ только для администраторов")
        else:
            try:
                data = int(data)
                client = db.sql_fetchone(
                    f"SELECT users.name FROM users inner join tickets on users.tg_id = tickets.client  WHERE tickets.id = {data}")
                contactor = db.sql_fetchone(
                    f"SELECT users.name FROM users inner join tickets on users.tg_id = tickets.contactor  WHERE tickets.id = {data}")
                ticket = db.sql_fetchall(
                    f"select id, category, cab,problem,category,status, t_new,t_progress,t_increase, t_completed from tickets where id={data}")
                if ticket[0]['status'] == "new":
                    status = "Новая"
                elif ticket[0]['status'] == 'closed':
                    status = "Закрыта"
                elif ticket[0]['status'] == 'in progress':
                    status = "В работе"
                elif ticket[0]['status'] == 'force closed':
                    status = "Закрыта тех.отделом"

                if ticket[0]['t_new'] is None:
                    t_new = "None"
                else:
                    t_new = datetime.fromtimestamp(int(ticket[0]['t_new'])).strftime("%d.%m.%Y %H:%M")

                if ticket[0]['t_progress'] is None:
                    t_progress = "None"
                else:
                    t_progress = datetime.fromtimestamp(int(ticket[0]['t_progress'])).strftime("%d.%m.%Y %H:%M")

                if ticket[0]['t_increase'] is None:
                    t_increase = "None"
                else:
                    t_increase = datetime.fromtimestamp(int(ticket[0]['t_increase'])).strftime("%d.%m.%Y %H:%M")

                if ticket[0]['t_completed'] is None:
                    t_completed = "None"
                else:
                    t_completed = datetime.fromtimestamp(int(ticket[0]['t_completed'])).strftime("%d.%m.%Y %H:%M")
                await message.answer(f"ID: {ticket[0]['id']}\n\n"
                                     f"Заявитель: {client}\n"
                                     f"Исполнитель: {contactor}\n\n"
                                     f"Статус: {status}\n"
                                     f"Проблема: {ticket[0]['problem']}\n\n"
                                     f"Инициирована: {t_new}\n"
                                     f"Взята в работу; {t_progress}\n"
                                     f"Передана выше: {t_increase}\n"
                                     f"Закрыта: {t_completed}\n"
                                     f"")
            except Exception as e:
                print("Exception:", e)
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
    dp.register_message_handler(start_cmd, commands=['start', 'ticket'])
    dp.register_message_handler(get_report, commands=['feedback'])
    dp.register_message_handler(get_ticket, commands=['id'])
    dp.register_message_handler(send_report, state=SendBugState.send_bug)
