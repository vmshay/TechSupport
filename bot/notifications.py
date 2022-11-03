from bot.dispatcher import bot
import bot.config as cnf
from bot.keyboards import tickets_kb, user_response


async def new_bug(data):
    msg = f"<b>Обратная связь</b>\n" \
          f"Сообщение: {data['bug']}\n" \
          f"Отправитель: {data['from_user']}\n"
    await bot.send_message(cnf.CHAT_ID, msg)


async def new_ticket(data):
    category = ''
    if data['Category'] == 'PC':
        category = '💻 Не включается ПК'
    if data['Category'] == 'deny_login':
        category = '🚪 Не входит в Moodle/ПК'
    if data['Category'] == 'no_internet':
        category = '🌐 Нет интернета'
    if data['Category'] == 'peripherals':
        category = '🖱️ Нужна периферия'
    if data['Category'] == 'printer':
        category = '🖨️ Не работает принтер'
    if data['Category'] == 'other':
        category = '❔ Другое '

    owner = data['name']
    cabinet = data['cab'].split(' ')[1]
    problem = data['problem']
    t_id = data['id']

    msg = f"<b>Новый тикет!</b>\n" \
          f"ID: {t_id}\n" \
          f"Отправитель: {owner}\n" \
          f"Категория: {category}\n" \
          f"Аудитория: {cabinet}\n" \
          f"Проблема: {problem}\n"
    await bot.send_message(cnf.CHAT_ID, msg, reply_markup=tickets_kb("accept", "deny", t_id))


async def notify_user_accept(u_id, t_id):
    msg = f"Заявка принята в работу\n" \
          f"Когда заявка будет выполненна подтвердите выполнение"
    await bot.send_message(u_id, msg, reply_markup=user_response(t_id))


async def notify_user_increase(u_id):
    msg = f"Статус заявки был изменен\n" \
          f"Для создания новой заявки нажмите /start"
    await bot.send_message(u_id, msg)


async def notify_user_force_close(u_id):
    msg = f"Заявка была закрыта тех.отделом\n" \
          f"Для создания новой заявки нажмите /start"
    await bot.send_message(u_id, msg)


async def notify_user_deny(u_id):
    msg = f"Заявка была отклонена\n" \
          f"Для создания новой заявки нажмите /start"
    await bot.send_message(u_id, msg)
