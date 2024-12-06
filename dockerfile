FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x joseco/manage.py

EXPOSE 8000

CMD ["python", "joseco/manage.py", "runserver", "0.0.0.0:8000"]
