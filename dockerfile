FROM python:3.12.3
ENV TOKEN='Токен из @BotFather'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]