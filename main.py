from aiogram.utils import executor
from bot.dispatcher import dp
import logging
import handlers.user.default
import handlers.admin
from bot import database

if __name__ == '__main__':
    if database.Database().__init__() is None:

        logging.basicConfig(level=logging.INFO)

        handlers.commands.main_register(dp)
        handlers.user.registration.register(dp)

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
        handlers.admin.increase_accept.register(dp)
        handlers.admin.accept_user.register(dp)
        handlers.admin.deny_user.register(dp)

        executor.start_polling(dp, skip_updates=True)
    else:
        print("Не удалось запустить бота")
