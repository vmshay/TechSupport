from aiogram import types, Dispatcher
from bot.keyboards import make_ticket_kb
from bot.States import TicketState
from aiogram.dispatcher.storage import FSMContext


async def printer(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Принтер", reply_markup=make_ticket_kb())
    await state.update_data(Category=call.data)
    await TicketState.category.set()


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(printer, text_startswith='printer', state=TicketState.init)
