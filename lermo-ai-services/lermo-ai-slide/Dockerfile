FROM python:3.10
RUN apt update
RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry lock && poetry install

EXPOSE 8082

ENTRYPOINT poetry run python main.py