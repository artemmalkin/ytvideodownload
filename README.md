# ytvideodownload
## Описание

YouTube Video Downloader Bot позволяет пользователям скачивать видео с YouTube, отправив ссылку на видео и выбрав желаемое разрешение. Бот обрабатывает видео и предоставляет ссылку для скачивания.

## Возможности

- Принимает ссылку на видео с YouTube и предлагает пользователю выбрать разрешение.
- Генерирует ссылку для скачивания видео в выбранном разрешении.

## Установка

### Шаг 1: Создание бота в Telegram

1. Откройте Telegram и найдите `@BotFather`.
2. Отправьте команду `/start` для начала взаимодействия.
3. Отправьте команду `/newbot` для создания нового бота.
4. Следуйте инструкциям для присвоения имени боту и получения токена API.

### Шаг 2: Клонирование репозитория

```sh
git clone https://github.com/yourusername/youtube-downloader-bot.git
cd youtube-downloader-bot
```

### Шаг 3: Установка зависимостей

#### Создание виртуального окружения

На Windows:
python -m venv venv

На macOS/Linux:
python3 -m venv venv

#### Активация виртуального окружения

На Windows:
.\venv\Scripts\activate

На macOS/Linux:
source venv/bin/activate

#### Установка необходимых пакетов

Убедитесь, что у вас установлен Python 3.7 или выше. Установите необходимые зависимости:

```sh
pip install -r requirements.txt
```

### Шаг 4: Настройка переменных окружения

Откройте файл `config.py` в корне проекта и добавьте в него ваш токен Telegram, полученный от `@BotFather`:

```python
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
```

### Шаг 5: Запуск бота

Запустите бота с помощью следующей команды:

```sh
python main.py
```

## Использование

1. Найдите своего бота в Telegram и отправьте команду `/start`.
2. Отправьте ссылку на видео с YouTube.
3. Выберите нужное разрешение из предложенных вариантов.
4. Получите ссылку для скачивания видео в выбранном разрешении.