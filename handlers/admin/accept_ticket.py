from aiogram import types, Dispatcher
from bot import database
from datetime import datetime
from bot.notifications import notify_user_accept
from bot.keyboards import increase_ticket


async def accept_ticket(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    client_id = db.sql_fetchone(f"select client from tickets where id = {t_id}")

    await call.message.edit_text(f"Исполнитель: {username}\n"
                                 f"ID заявки: {t_id}\n"
                                 f"Время: {timestamp}\n", reply_markup=increase_ticket(t_id))

    db.sql_query_send(f"update tickets set contactor = {call.from_user.id}, t_progress = '{timestamp}',"
                      f"status='in progress' where id = {t_id}")
    await notify_user_accept(client_id, t_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(accept_ticket, text_startswith='accept:')
