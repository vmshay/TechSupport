from datetime import datetime
from aiogram import types, Dispatcher
from bot import database
from bot.notifications import notify_user_deny
import time


async def deny_ticket(call: types.CallbackQuery):
    t_id = call.data.split(":")[1]
    db = database.Database()
    timestamp = int(time.time())
    u_time = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    client_id = db.sql_fetchone(f"select client from tickets where id = {t_id}")
    db.sql_query_send(f"update tickets set contactor = {call.from_user.id}, t_completed = '{timestamp}',"
                      f"status='deny' where id = {t_id}")

    await call.message.edit_text(f"{username} отклонил заявку\n"
                                 f"ID заявки: {t_id}\n"
                                 f"Дата: {u_time}\n")
    await notify_user_deny(client_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(deny_ticket, text_startswith='deny:')
