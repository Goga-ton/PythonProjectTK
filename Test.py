import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота (замените на ваш)
BOT_TOKEN = "grgwregrgregre"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранение активных таймеров в памяти
active_timers = {}


@dp.message(Command("timer"))
async def cmd_timer(message: Message):
    try:
        # Получаем аргумент команды
        args = message.text.split()
        if len(args) < 2:
            await message.answer("Использование: /timer <время> (например: /timer 10m)")
            return

        time_arg = args[1].lower()

        # Проверяем формат времени
        if not time_arg.endswith('m'):
            await message.answer("Неверный формат времени. Используйте число + m (например: 10m)")
            return

        # Извлекаем количество минут
        minutes = int(time_arg[:-1])
        if minutes <= 0:
            await message.answer("Время должно быть положительным числом")
            return

        user_id = message.from_user.id
        chat_id = message.chat.id

        # Отменяем предыдущий таймер пользователя, если есть
        if user_id in active_timers:
            active_timers[user_id].cancel()
            logger.info(f"Предыдущий таймер для пользователя {user_id} отменен")

        # Создаем и запускаем новый таймер
        timer_task = asyncio.create_task(timer_countdown(user_id, chat_id, minutes))
        active_timers[user_id] = timer_task

        await message.answer(f"Таймер на {minutes} минут установлен")
        logger.info(f"Таймер на {minutes} минут установлен для пользователя {user_id}")

    except ValueError:
        await message.answer("Неверный формат времени. Используйте число + m (например: 10m)")
    except Exception as e:
        logger.error(f"Ошибка при установке таймера: {e}")
        await message.answer("Произошла ошибка при установке таймера")


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message):
    user_id = message.from_user.id

    if user_id in active_timers:
        # Отменяем таймер
        active_timers[user_id].cancel()
        del active_timers[user_id]

        await message.answer("Таймер отменён")
        logger.info(f"Таймер для пользователя {user_id} отменен")
    else:
        await message.answer("У вас нет активных таймеров")


async def timer_countdown(user_id: int, chat_id: int, minutes: int):
    """
    Асинхронная функция таймера
    """
    try:
        # Ждем указанное количество минут
        await asyncio.sleep(minutes * 60)

        # Проверяем, не был ли таймер отменен
        if user_id in active_timers:
            # Отправляем сообщение о завершении таймера
            await bot.send_message(chat_id, "Время вышло!")
            logger.info(f"Таймер для пользователя {user_id} завершен")

            # Удаляем таймер из активных
            if user_id in active_timers:
                del active_timers[user_id]

    except asyncio.CancelledError:
        # Таймер был отменен - это нормально
        logger.info(f"Таймер для пользователя {user_id} был отменен во время ожидания")
    except Exception as e:
        logger.error(f"Ошибка в таймере для пользователя {user_id}: {e}")


async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())