from datetime import datetime
from aiogram import types, Dispatcher
from bot import database

async def deny_ticket(call: types.CallbackQuery):
    t_id = call.data.split(":")[1]
    db = database.Database()
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    await call.message.edit_text(f"{username} отклонил заявку\n"
                                 f"ID заявки: {t_id}\n"
                                 f"Время: {timestamp}\n")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(deny_ticket, text_startswith='i_deny:')
