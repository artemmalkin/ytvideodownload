# Импортируем необходимые модули для работы с ботом Telegram, YouTube и логированием
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pytube import YouTube
from config import TELEGRAM_TOKEN

# Настройка системы логирования для отслеживания событий и ошибок в процессе работы бота
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для получения ссылки на скачивание видео
def get_download_link(youtube_url):
    try:
        # Создаем объект YouTube с использованием переданной URL-адреса
        yt = YouTube(youtube_url)
        
        # Выбираем поток видео. В данном случае, выбираем первый поток с прогрессивной загрузкой (аудио и видео в одном файле)
        # и с наивысшим разрешением.
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        # Получаем ссылку для скачивания этого потока
        download_url = stream.url
        
        return download_url
    except Exception as e:
        # Если возникла ошибка, печатаем её и обрабатываем случай возрастного ограничения
        print(f"Произошла ошибка: {e}")
        if "age restricted" in str(e):
            return "Извините, это видео имеет возрастное ограничение и не может быть скачано."
        return None

# Асинхронная функция-обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем приветственное сообщение пользователю
    await update.message.reply_text("Привет, чтобы скачать видео из YouTube, отправь мне ссылку на видео.")

# Асинхронная функция-обработчик для обработки сообщений с YouTube ссылками
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем текст сообщения от пользователя, это должна быть YouTube ссылка
    youtube_url = update.message.text
    
    # Пытаемся получить ссылку для скачивания
    download_link = get_download_link(youtube_url)
    
    # В зависимости от результата формируем ответное сообщение
    if download_link is None:
        message = "Не удалось получить ссылку для скачивания. Проверьте правильность URL или попробуйте позже."
    elif "извините" in download_link.lower():
        message = download_link  # сообщение о возрастном ограничении
    else:
        message = f"Вот ваша ссылка для скачивания: {download_link}"
    
    # Отправляем ответное сообщение пользователю
    await update.message.reply_text(message)

# Основная часть программы
if __name__ == '__main__':
    # Создаем экземпляр приложения для бота, используя токен из конфигурационного файла
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Создаем обработчик команды /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Создаем обработчик для текстовых сообщений, исключая команды
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    # Запускаем бота и начинаем прослушивать сообщения
    application.run_polling()