from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    create_ticket = InlineKeyboardButton('🎫 Создать заявку', callback_data='init')
    status_ticket = InlineKeyboardButton('Статус заявок', callback_data='status')
    keyboard.add(create_ticket, status_ticket)
    return keyboard


def default_tickets_kb():
    keyboard = InlineKeyboardMarkup()
    pc = InlineKeyboardButton('💻 Не включается ПК', callback_data='PC')
    not_enter = InlineKeyboardButton('🚪 Не входит в Moodle/ПК', callback_data='deny_login')
    not_internet = InlineKeyboardButton('🌐 Нет интернета', callback_data='no_internet')
    need = InlineKeyboardButton('🖱️ Нужна периферия', callback_data='peripherals')
    printer = InlineKeyboardButton('🖨️ Не работает принтер', callback_data='printer')
    other = InlineKeyboardButton('❔ Другое ', callback_data='other')

    keyboard.add(pc)
    keyboard.add(not_enter)
    keyboard.add(need)
    keyboard.add(printer)
    keyboard.add(not_internet)
    keyboard.add(other)
    return keyboard


def make_ticket_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    make_ticket = InlineKeyboardButton('✏️Создать заявку', callback_data='make_ticket')
    main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
    keyboard.add(make_ticket)
    keyboard.add(main_menu)
    return keyboard


def floor_kb():
    keyboard = InlineKeyboardMarkup()
    floor_1 = InlineKeyboardButton('Первый этаж', callback_data='Floor1')
    floor_2 = InlineKeyboardButton('Второй этаж', callback_data='Floor2')
    floor_3 = InlineKeyboardButton('Третий этаж', callback_data='Floor3')
    floor_4 = InlineKeyboardButton('Четвертый этаж', callback_data='Floor4')
    floor_b2 = InlineKeyboardButton('Второй корпус', callback_data="Floor_B2")
    main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
    keyboard.add(floor_4)
    keyboard.add(floor_3)
    keyboard.add(floor_2)
    keyboard.add(floor_1)
    keyboard.add(floor_b2)
    keyboard.add(main_menu)
    return keyboard


def cabinets_kb(floor):
    floor1 = ['Ауд. 101', 'Ауд. 103',
              'Ауд. 106', 'Ауд. 112']

    floor2 = ['Ауд. 201', 'Ауд. 202', 'Ауд. 203',
              'Ауд. 205', 'Ауд. 207', 'Ауд. 208',
              'Ауд. 209', 'Ауд. 210', 'Ауд. 211']

    floor3 = ['Ауд. 301', 'Ауд. 302', 'Ауд. 303',
              'Ауд. 304', 'Ауд. 305', 'Ауд. 306',
              'Ауд. 307', 'Ауд. 308', 'Ауд. 309']

    floor4 = ['Ауд. 401', 'Ауд. 402', 'Ауд. 403',
              'Ауд. 404', 'Ауд. 405', 'Ауд. 407']

    build2 = ['Ауд. 48', 'Ауд. 49', 'Ауд. 56',
              'Ауд. 57', 'Ауд. 58', 'Ауд. 61']

    keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)

    if floor == "Floor1":
        keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        for cab in floor1:
            key = InlineKeyboardButton(text=cab, callback_data=cab)
            keyboard.insert(key)
        main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
        keyboard.add(main_menu)
        return keyboard

    if floor == "Floor2":

        for cab in floor2:
            key = InlineKeyboardButton(text=cab, callback_data=cab)
            keyboard.insert(key)
        main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
        keyboard.add(main_menu)
        return keyboard

    if floor == "Floor3":
        for cab in floor3:
            key = InlineKeyboardButton(text=cab, callback_data=cab)
            keyboard.insert(key)
        main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
        keyboard.add(main_menu)
        return keyboard

    if floor == "Floor4":
        for cab in floor4:
            key = InlineKeyboardButton(text=cab, callback_data=cab)
            keyboard.insert(key)
        main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
        keyboard.add(main_menu)
        return keyboard
    if floor == "Floor_B2":
        for cab in build2:
            key = InlineKeyboardButton(text=cab, callback_data=cab)
            keyboard.insert(key)
        main_menu = InlineKeyboardButton('↩️Вернуться в меню', callback_data='main_menu')
        keyboard.add(main_menu)
        return keyboard


def tickets_kb():
    keyboard = InlineKeyboardMarkup()
    accept = InlineKeyboardButton("Принять",callback_data='accept')
    deny = InlineKeyboardButton("Отклонить",callback_data='deny')
    keyboard.add(accept, deny)
    return keyboard
