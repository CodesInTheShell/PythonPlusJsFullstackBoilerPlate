### Build the Docker image
# docker build -t flask-app .

### Run the Docker container
# docker run -p 8000:8000 flask-app

FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]