from aiogram import types, Dispatcher
from bot import database
import time
from datetime import datetime


async def accept_ticket(call: types.CallbackQuery):
    st = time.time()
    t_id = call.data.split(":")[1]
    db = database.Database()
    date = datetime.now().date()
    t_progress = datetime.now().time().strftime("%H:%M")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    await call.message.edit_text(f"Исполнитель: {username}\n"
                                 f"ID заявки: {t_id}\n"
                                 f"Дата: {date}\n"
                                 f"Время: {t_progress}")
    print("DEBUG: Accept ID", t_id)
    et = time.time()
    print(f"DEBUG: Время подтверждения заявки: {et - st}")
    print("В работе с ", t_progress)
    # TODO: отправка сообщения заявителю


async def deny_ticket(call: types.CallbackQuery):
    t_completed = datetime.now().time().strftime("%H:%M")
    t_id = call.data.split(":")[1]
    await call.message.edit_text(f"{call.from_user.id} забрал заявку")
    print("deny", t_id)
    print("Отменена в ", t_completed)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(accept_ticket, text_startswith='accept:')
    dp.register_callback_query_handler(deny_ticket, text_startswith='deny:')
