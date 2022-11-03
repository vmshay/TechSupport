import asyncio
from aiogram import types, Dispatcher
from bot.keyboards import default_tickets_kb, cabinets_kb, main_kb, floor_kb
from aiogram.dispatcher.storage import FSMContext
from bot.States import TicketState
from bot.notifications import new_ticket
from datetime import datetime
from bot import database, sql


async def return_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print("FSM сброшен")
    await call.message.edit_text(f"🤖Вас приветствует бот технической поддержки ТТИТ🤖\n"
                                 f"\n"
                                 f"Для того чтобы сформировать заявку нажмите кнопку ниже.\n\n"
                                 f"Так же вы можете узнать статус заявки.\n\n"
                                 f"Если есть пожелания или замечания\n"
                                 f"Можете обратиться к @FeldwebelWillman\n"
                                 f"Или воспользовтаься обратной связью /feedback",
                                 reply_markup=main_kb())


async def init_ticket(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите категорию обращения", reply_markup=default_tickets_kb())
    db = database.Database()
    username = db.sql_fetchone(f"select name from users where tg_id = {call.from_user.id}")
    await TicketState.init.set()
    await state.update_data(tg_id=call.from_user.id)
    await state.update_data(name=username)


async def choose_floor(call: types.CallbackQuery):
    await call.message.edit_text("Выберите этаж", reply_markup=floor_kb())
    await TicketState.Floor.set()


async def choose_cabinet(call: types.CallbackQuery):
    await call.message.edit_text("Выберите аудиторию", reply_markup=cabinets_kb(call.data))
    await TicketState.Cab.set()


async def get_problem(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text("Опишите проблему")
    await state.update_data(cab=call.data)
    await TicketState.Problem.set()
    await asyncio.sleep(30)
    await msg.delete()


async def send_report(message: types.Message, state: FSMContext):
    db = database.Database()
    await message.delete()
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    await state.update_data(problem=message.text)
    await state.update_data(t_new=timestamp)
    await state.update_data(status='new')
    msg = await message.answer("Заявка направлена в технический отдел")
    data = await state.get_data()
    db.sql_query_send(sql=sql.send_ticket(data))
    ticket_id = db.sql_fetchone('select max(id) from tickets')
    await state.update_data(id=ticket_id)
    data = await state.get_data()
    await state.finish()
    await new_ticket(data)
    await asyncio.sleep(20)
    await msg.delete()


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(init_ticket, text='init')
    dp.register_callback_query_handler(return_menu, text='main_menu', state=[TicketState.init, TicketState.Cab,
                                                                             TicketState.make_ticket, TicketState.Floor,
                                                                             TicketState.category])
    dp.register_callback_query_handler(choose_floor, text='make_ticket', state=TicketState.category)
    dp.register_callback_query_handler(choose_cabinet, text_startswith='Floor', state=TicketState.Floor)
    dp.register_callback_query_handler(get_problem, text_startswith='Ауд.', state=TicketState.Cab)
    dp.register_message_handler(send_report, state=TicketState.Problem)
