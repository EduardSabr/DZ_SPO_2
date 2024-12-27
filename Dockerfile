FROM python

# Устанавливаем рабочую директорию
WORKDIR /bot

# Копируем файлы проекта в контейнер
COPY . /bot

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Запускаем приложение
CMD ["python","sabrekovspobot.py"]