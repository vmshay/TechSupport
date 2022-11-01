from aiogram.dispatcher.filters.state import StatesGroup, State


class SendBugState(StatesGroup):
    send_bug = State()


class TicketState(StatesGroup):
    init = State()
    category = State()
    make_ticket = State()
    Floor = State()
    Cab = State()
    Problem = State()
