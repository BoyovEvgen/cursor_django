FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./docker/python/wait-for-it.sh /app

#ENTRYPOINT "./docker/python/entrypoint.sh"

CMD .wait-for-it.sh db:3306 -- python3 manage.py runserver 0.0.0.0:8000 -- python3 ./telegram_bot/management/commands/polling.py
