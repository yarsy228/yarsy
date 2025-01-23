import telebot
from datetime import datetime
import time
import asyncio

# Укажи свой токен бота
BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"  # ID чата, куда бот будет отправлять сообщения
POSTS_FILE = "posts.txt"  # Имя файла с постами

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для чтения постов из файла
def read_posts():
    posts = []
    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            try:
                datetime_str, message = line.split(": ", 1)
                post_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                posts.append((post_time, message.strip()))
            except ValueError:
                print(f"Ошибка в строке: {line.strip()}")
    return posts

# Асинхронная функция для отправки постов
async def schedule_posts():
    while True:
        posts = read_posts()
        now = datetime.now()
        for post_time, message in posts:
            if post_time <= now:
                try:
                    bot.send_message(CHAT_ID, message)
                    print(f"Отправлено: {message}")
                except Exception as e:
                    print(f"Ошибка отправки сообщения: {e}")
                # Удаляем отправленный пост из файла
                with open(POSTS_FILE, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                with open(POSTS_FILE, "w", encoding="utf-8") as file:
                    for line in lines:
                        if message not in line:
                            file.write(line)
        await asyncio.sleep(60)  # Проверяем каждые 60 секунд

# Запуск
if __name__ == "__main__":
    print("Бот запущен. Ожидание сообщений...")
    asyncio.run(schedule_posts())
