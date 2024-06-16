# Импортируем необходимые модули для работы с ботом Telegram, YouTube и логированием
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from pytube import YouTube
from config import TELEGRAM_TOKEN

# Настройка системы логирования для отслеживания событий и ошибок в процессе работы бота
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для создания клавиатуры с кнопками для выбора разрешения видео
def create_resolution_keyboard(yt, url):
    keyboard = []
    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    for stream in streams:
        res = stream.resolution
        # Сохраняем в callback data как разрешение, так и url
        keyboard.append([InlineKeyboardButton(res, callback_data=f"{res}|{url}")])

    return InlineKeyboardMarkup(keyboard)

# Асинхронная функция-обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем приветственное сообщение пользователю
    await update.message.reply_text("Привет, чтобы скачать видео из YouTube, отправь мне ссылку на видео.")

# Асинхронная функция-обработчик для обработки сообщений с YouTube ссылками
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем текст сообщения от пользователя, это должна быть YouTube ссылка
    youtube_url = update.message.text
    
    try:
        # Сообщаем пользователю об ожидании
        await update.message.reply_text("Обрабатываю видео, пожалуйста, подождите...")

        # Создаем объект YouTube с использованием переданной URL-адреса
        yt = YouTube(youtube_url)

        # Создаем и отправляем клавиатуру с доступными разрешениями
        reply_markup = create_resolution_keyboard(yt, youtube_url)
        await update.message.reply_text("Выберите разрешение:", reply_markup=reply_markup)
    except Exception as e:
        # Если возникла ошибка, печатаем её и обрабатываем случай возрастного ограничения
        print(f"Произошла ошибка: {e}")
        if "age restricted" in str(e):
            await update.message.reply_text("Извините, это видео имеет возрастное ограничение и не может быть скачано.")
        else:
            await update.message.reply_text("Не удалось получить ссылку для скачивания. Проверьте правильность URL или попробуйте позже.")

# Асинхронная функция-обработчик для обработки нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query_data = query.data.split('|')  # Разделяем callback data на разрешение и URL

    if len(query_data) != 2:
        await query.edit_message_text(text="Произошла ошибка при обработке данных. Попробуйте ещё раз.")
        return

    resolution, youtube_url = query_data

    try:
        # Сообщаем пользователю об ожидании
        await query.edit_message_text(text="Получаю ссылку для скачивания, пожалуйста, подождите...")

        # Создаем объект YouTube с использованием переданной URL-адреса
        yt = YouTube(youtube_url)

        # Выбираем поток видео с выбранным разрешением
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        
        # Получаем ссылку для скачивания этого потока
        download_url = stream.url
        
        # Формируем ответное сообщение
        message = f"Вот ваша ссылка для скачивания: {download_url}"

        # Редактируем сообщение с кнопками, чтобы показать результат
        await query.edit_message_text(text=message)
    except Exception as e:
        # Если возникла ошибка, печатаем её и обрабатываем случай возрастного ограничения
        print(f"Произошла ошибка: {e}")

        
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

    # Создаем обработчик для обработчика нажатий на кнопки
    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)

    # Запускаем бота и начинаем прослушивать сообщения
    application.run_polling()