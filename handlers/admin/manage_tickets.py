from bot.dispatcher import bot
import bot.config as cnf
from bot.keyboards import tickets_kb




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

    owner = data['tg_id']
    cabinet = data['Cab'].split(' ')[1]
    problem = data['Problem']

    msg = f"Ноывй тикет!\n" \
          f"Отправитель: {owner}\n" \
          f"Категория: {category}\n" \
          f"Аудитория: {cabinet}\n" \
          f"Проблема: {problem}\n"
    await bot.send_message(cnf.CHAT_ID, msg, reply_markup=tickets_kb())



async def accept_ticket