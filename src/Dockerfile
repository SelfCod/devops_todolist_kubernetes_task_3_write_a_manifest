FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure to run migrations
RUN python manage.py migrate

EXPOSE 8000

# Explicitly bind to 0.0.0.0
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
