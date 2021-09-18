FROM python:3.9
RUN mkdir -p /bot
WORKDIR /bot
COPY pyproject.toml poetry.lock /bot/
RUN pip3 install poetry
ENV POETRY_VIRTUALENVS_CREATE false
COPY . /bot
RUN poetry install
RUN chmod +x scripts/*
ENTRYPOINT ["scripts/docker-entrypoint.sh"]