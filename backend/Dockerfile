FROM python:3-slim

WORKDIR /app



ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1\
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false 



RUN apt-get update && apt-get install -y \
    curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY backend/.dockerignore ./
COPY  backend/pyproject.toml backend/poetry.lock ./

RUN poetry install --no-root 

COPY backend/src ./src
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]