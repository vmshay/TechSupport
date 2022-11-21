from aiogram import types, Dispatcher
from bot import database
from datetime import datetime
from bot.notifications import notify_user_accept
from bot.keyboards import increase_ticket
import time


async def accept_ticket(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    timestamp = int(time.time())
    u_time = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    client_id = db.sql_fetchone(f"select client from tickets where id = {t_id}")
    ticket = db.sql_fetchall(f"select category, cab,problem,category from tickets where id={t_id}")
    
    if ticket[0]['category'] == 'PC':
        category = '  Не включается ПК'
    if ticket[0]['category'] == 'deny_login':
        category = '  Не входит в Moodle/ПК'
    if ticket[0]['category'] == 'no_internet':
        category = '  Нет интернета'
    if ticket[0]['category'] == 'peripherals':
        category = '  Нужна периферия'
    if ticket[0]['category'] == 'printer':
        category = '  Не работает принтер'
    if ticket[0]['category'] == 'other':
        category = '  Другое '
    if ticket[0]['category'] == 'projector':
        category = '  Не работает проектор'

    print("accept ticket")
    await call.message.edit_text(f"ID: {t_id}\n\n"
                                 f"Заявитель: {username}\n"
                                 f"Исполнитель: {username}\n\n"
                                 f"Аудитория: {ticket[0]['cab']}\n"
                                 f"Категория: {category}\n"
                                 f"Комментарий: {ticket[0]['problem']}\n\n"
                                 f"Взята в работу: {u_time}\n", reply_markup=increase_ticket(t_id))

    db.sql_query_send(f"update tickets set contactor = {call.from_user.id}, t_progress = '{timestamp}',"
                      f"status='in progress' where id = {t_id}")
    await notify_user_accept(client_id, t_id, username)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(accept_ticket, text_startswith='accept:')
    # dp.register_callback_query_handler(accept_ticket, text_startswith='i_accept:')
