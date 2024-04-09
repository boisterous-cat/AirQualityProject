FROM python:3.11-slim

COPY ./ /tgBot
COPY requirements.txt /tgBot

WORKDIR /tgBot

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]