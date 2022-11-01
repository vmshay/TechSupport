from aiogram.utils import executor
from bot.dispatcher import dp
import logging
import handlers.user
import handlers.user.default


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    handlers.Start.main_register(dp)
    handlers.user.make_ticket.register_handlers(dp)
    handlers.user.default.PCNotWork.register_handlers(dp)
    handlers.user.default.NoInternet.register_handlers(dp)
    handlers.user.default.Other.register_handlers(dp)
    handlers.user.default.Peripherals.register_handlers(dp)
    handlers.user.default.Printer.register_handlers(dp)
    handlers.user.default.DenyLogin.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
