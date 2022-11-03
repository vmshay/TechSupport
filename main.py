from aiogram.utils import executor
from bot.dispatcher import dp
import logging
import handlers.user.default
import handlers.admin

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
    handlers.user.close_ticket.register(dp)
    handlers.admin.accept_ticket.register(dp)
    handlers.admin.deny_ticket.register(dp)
    handlers.admin.force_close.register(dp)
    handlers.admin.increase_ticket.register(dp)

    executor.start_polling(dp, skip_updates=True)
