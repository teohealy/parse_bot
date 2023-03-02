from aiogram import Bot, Dispatcher, executor, types
from config import token


bot = Bot(token=token)
dp = Dispatcher(bot)

HELP_COMMAND = '''
<b>Выберете, интересующую категорию:</b>
<b>/help</b> - <em>Список команд</em>
<b>/start</b> - <em>Запуск бота</em>
<b>/info</b> - <em>Информация о боте</em>

<b>/cars</b> - <em>Поиск автомобиля</em>
<b>/spares</b> - <em>Поиск запчастей</em>
<b>/tires</b> - <em>Поиск шин</em>


<b>/news</b> - <em>Новости мира авто</em>

<b>/photo</b> - <em>Получить фото авто</em> 
'''


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMAND, parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)