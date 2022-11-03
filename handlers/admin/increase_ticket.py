from aiogram import types, Dispatcher
from bot.keyboards import tickets_kb
from bot import database
from datetime import datetime
from bot.notifications import notify_user_increase


async def increase_ticket(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    db.sql_query_send(f"update tickets set status = 'increased', t_increase = '{timestamp}' where id={t_id}")
    client_id = db.sql_fetchone(f"select client from tickets where id = {t_id}")
    status = db.sql_fetchone(f'select status from tickets where id = {t_id}')
    # username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")

    if status != 'closed':
        db.sql_query_send(f"update tickets set t_completed = '{timestamp}',status = 'closed' where id = {t_id}")
        db.sql_query_send(f"update tickets set status='force closed',t_completed = '{timestamp}' where id={t_id}")
        await call.message.edit_text(f"Заявка закрыта поьзователем\n"
                                     f"ID заявки: {t_id}\n"
                                     f"Время {timestamp}\n")
    else:
        await call.message.edit_text(f"Статус заявки повышен\n"
                                     f"@hexfavorite\n"
                                     f"@Locotb\n"
                                     f"@FeldwebelWillman", reply_markup=tickets_kb("i_accept", "i_deny", t_id))
        await notify_user_increase(client_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(increase_ticket, text_startswith="increase:")
