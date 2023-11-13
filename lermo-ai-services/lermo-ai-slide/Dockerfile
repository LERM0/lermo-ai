FROM lerm0/lermo-ai-slide

WORKDIR /app

COPY . .

RUN poetry install

EXPOSE 8080

ENTRYPOINT poetry run python main.py