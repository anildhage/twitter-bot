FROM python:3.6.13-alpine

COPY config.py /bot/
COPY bot.py /bot/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bot
CMD ["python3", "bot.py"]