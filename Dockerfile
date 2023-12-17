FROM node:18-slim as WEB
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY ./web /app
WORKDIR /app
RUN ls
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

FROM python:3.11.7-slim
RUN pip install poetry
RUN mkdir -p /app/web/build

COPY ./pyproject.toml ./poetry.lock ./README.md /app/
COPY ./src /app/src/
COPY --from=WEB /app/build /app/web/build
WORKDIR /app

RUN poetry install

EXPOSE 8000
ENV FLASK_APP = src/flaskr/__init__.py
ENV FLASK_ENV = production
CMD ["poetry", "run", "python", "-m", "flask", "run", "--port", "8000", "--host", "0.0.0.0"]