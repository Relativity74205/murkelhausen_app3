FROM python:3.13-slim-bullseye AS base

RUN apt-get update && \
    # libpq-dev for psycopg
    apt-get install -y --no-install-recommends curl libpq-dev && \
    apt-get clean && \
    (rm -rf /var/lib/apt/lists/* || true)


RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="${PATH}:/root/.local/bin"

FROM base AS prod

WORKDIR /usr/app

COPY family_intranet family_intranet
COPY core core
COPY entrypoint.sh manage.py pyproject.toml uv.lock* README.md ./

RUN uv sync --locked

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000
