from bot.dispatcher import bot
import bot.config as cnf


async def new_bug(data):
    msg = f"<b>Обратная связь</b>\n" \
          f"Сообщение: {data['bug']}\n" \
          f"Отправитель: {data['from_user']}\n"
    await bot.send_message(cnf.CHAT_ID, msg)



