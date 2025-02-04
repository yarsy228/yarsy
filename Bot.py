import json
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import logging
import asyncio
from aiogram import Bot

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()

# Ваш токен Telegram-бота
TOKEN = "7034379788:AAFb9inCGM8zuR8ZeatdjkjQu0xiqcQuI3A"  # Замість ВАШ_ТОКЕН_БОТА вставте реальний токен
CHAT_ID = "-1002300323926"  # ID чата або користувача, куди надсилати повідомлення

# Ініціалізація Telegram-бота
bot = Bot(token=TOKEN)

# Функція для публікації поста
async def publish_post(post_text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=post_text)
        logging.info(f"Пост відправлено: {post_text}")
    except Exception as e:
        logging.error(f"Помилка при відправці поста: {e}")

# Завантаження постів із файлу
def load_posts(file_path="posts.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Планування постів
def schedule_posts(posts):
    for post in posts:
        post_time = datetime.strptime(post["datetime"], "%Y-%m-%d %H:%M:%S")
        scheduler.add_job(
            publish_post,
            DateTrigger(run_date=post_time),
            args=[post["text"]],
            id=f"post_{post_time}",  # Унікальний ID задачі
            replace_existing=True
        )
        logging.info(f"Заплановано пост: '{post['text']}' на {post['datetime']}")

# Основна асинхронна функція
async def main():
    posts = load_posts()
    schedule_posts(posts)
    scheduler.start()
    logging.info("Бот запущено")

    # Блокування виконання програми для безперервної роботи
    await asyncio.Event().wait()

# Запуск програми
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот зупинено")
