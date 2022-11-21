from bot import database
from aiogram import Dispatcher, types
from bot.notifications import notify_admins_close
import time


async def close_ticket(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    timestamp = int(time.time())
    status = db.sql_fetchone(f'select status from tickets where id = {t_id}')

    if status != 'force closed':
        db.sql_query_send(f"update tickets set t_completed = '{timestamp}',status = 'closed' where id = {t_id}")
        await call.message.edit_text(f"Заявка №{t_id} закрыта")
        await notify_admins_close(t_id)
    else:
        await call.message.edit_text(f"Заявка №{t_id} закрыта тех. отделом")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(close_ticket, text_startswith="closed:")
