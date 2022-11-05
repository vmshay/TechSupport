from aiogram import types, Dispatcher
from bot import database
from datetime import datetime
from bot.notifications import notify_user_force_close
import time


async def force_close(call: types.CallbackQuery):
    t_id = call.data.split(":")[1]
    db = database.Database()

    timestamp = int(time.time())
    u_time = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    client_id = db.sql_fetchone(f"select client from tickets where id = {t_id}")
    status = db.sql_fetchone(f'select status from tickets where id = {t_id}')

    if status != 'closed':
        db.sql_query_send(f"update tickets set status='force closed',t_completed = '{timestamp}' where id={t_id}")
        await call.message.edit_text(f"{username} принудительно закрыл заявку\n"
                                     f"ID заявки: {t_id}\n"
                                     f"Дата: {u_time}\n")
        await notify_user_force_close(client_id)
    else:
        await call.message.edit_text(f"Заявка закрыта пользователем\n"
                                     f"ID заявки: {t_id}\n"
                                     f"Дата: {timestamp}\n")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(force_close, text_startswith="force:")
