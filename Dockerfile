FROM python:3.7.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV PYTHONPATH=/app
ENV PORT 8000

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libgl1-mesa-dev
WORKDIR /app
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn flashcard.wsgi:application
