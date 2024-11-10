### Build the Docker image
# docker build -t django-app .

### Run migrations
# docker run --rm django-app python manage.py makemigrations
# docker run --rm django-app python manage.py migrate

### Run the Docker container
# docker run -p 8000:8000 django-app


FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev libc-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
