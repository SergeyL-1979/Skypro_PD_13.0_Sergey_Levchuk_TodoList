# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.10-slim

# Устанавливает рабочий каталог контейнера — "code"
RUN mkdir /code
WORKDIR /code

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Копирует все файлы из нашего локального проекта в контейнер
RUN pip install --upgrade pip
COPY requirements.txt /code/

# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
RUN pip install -r requirements.txt

# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, в рабочую директорию контейнера
COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]