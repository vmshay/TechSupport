import asyncio
from aiogram import types, Dispatcher
from bot.keyboards import default_tickets_kb, cabinets_kb, main_kb, floor_kb
from aiogram.dispatcher.storage import FSMContext
from bot.States import TicketState


async def return_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print("FSM сброшен")
    await call.message.edit_text(f"🤖Вас приветствует бот технической поддержки🤖\n"
                                 f"\n"
                                 f"Для того чтобы сформировать заявку нажмите кнопку ниже.\n\n"
                                 f"Так же вы можете узнать статус заявки.\n\n"
                                 f"Если есть пожелания или замечания\n"
                                 f"Можете обратиться к @FeldwebelWillman\n"
                                 f"Или воспользовтаься обратной связью /feedback",
                                 reply_markup=main_kb())


async def init_ticket(call: types.CallbackQuery,state: FSMContext):
    await call.message.edit_text("Выберите категорию обращения", reply_markup=default_tickets_kb())
    await TicketState.init.set()
    await state.update_data(tg_id=call.from_user.id)


async def choose_floor(call: types.CallbackQuery, ):
    await call.message.edit_text("Выберите этаж", reply_markup=floor_kb())
    await TicketState.Floor.set()


async def choose_cabinet(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите аудиторию", reply_markup=cabinets_kb(call.data))
    await state.update_data(Floor=call.data)
    await TicketState.Cab.set()


async def get_problem(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text("Опишите проблему")
    await state.update_data(Cab=call.data)
    await TicketState.Problem.set()
    await asyncio.sleep(30)
    await msg.delete()


async def send_report(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(Problem=message.text)
    msg = await message.answer("Заявка направлена в технический отдел")
    data = await state.get_data()
    await state.finish()
    await message.answer(data)
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
