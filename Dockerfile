# указываем язык прогромирования
FROM python:3.10

# копировать все папки/файлы в Докер
COPY . /pay_system

# установка необходиммых компонентов
RUN pip install -r requirements.txt

# команда для запуска
CMD ["uvicorn", "main:app", "--host:0.0.0.0", "--port=8080"]