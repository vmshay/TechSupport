from aiogram import types, Dispatcher
from bot import database
from datetime import datetime
from bot.keyboards import force_close
import time


async def accept_ticket(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    timestamp = int(time.time())
    u_time = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")

    await call.message.edit_text(f"Исполнитель: {username}\n"
                                 f"ID заявки: {t_id}\n"
                                 f"Дата: {u_time}\n", reply_markup=force_close(t_id))

    db.sql_query_send(f"update tickets set contactor = {call.from_user.id}, t_progress = '{timestamp}',"
                      f"status='in progress' where id = {t_id}")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(accept_ticket, text_startswith='i_accept:')
