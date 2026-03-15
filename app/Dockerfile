FROM python:3.11-slim

# Установка системных зависимостей для аудио и tensorflow
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libsndfile1-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папки
RUN mkdir -p uploads static/models

# Экспонируем порт
EXPOSE 5000

# Инициализация БД и запуск
CMD ["sh", "-c", "python database.py && python main.py"]
