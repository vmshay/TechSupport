from bot import database
from aiogram import Dispatcher, types
from datetime import datetime


async def close_ticket(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    status = db.sql_fetchone(f'select status from tickets where id = {t_id}')
    if status != 'force closed':
        db.sql_query_send(f"update tickets set t_completed = '{timestamp}',status = 'closed' where id = {t_id}")
        await call.message.edit_text("Заявка закрыта")
    else:
        await call.message.edit_text("Заявка была закрыта тех. отделом")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(close_ticket, text_startswith="closed:")
