# Hint 
# https://github.com/python-poetry/poetry/discussions/1879
# https://www.mktr.ai/the-data-scientists-quick-guide-to-dockerfiles-with-examples/
# Using multistage builds with smaller base image reduced from 1.49GB to 539MB

###############################################
# Base Image
###############################################
FROM python:3.11.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.6.1  \
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # location of requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" 

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base
RUN apt-get -qy update \
    && apt-get -qy install --no-install-recommends openssl netcat curl build-essential

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3

# Copy project requirement files.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml wait-for.sh ./
COPY ./app ./app
COPY ./scripts ./scripts

# Install runtime dependencies. uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --only main

###############################################
# Production Image
###############################################
FROM python-base as production
RUN apt-get -qy update \
    && apt-get -qy install --no-install-recommends openssl netcat-traditional curl build-essential

ENV PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" 

WORKDIR $PYSETUP_PATH
# COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./prisma ./prisma
RUN pip install prisma
RUN prisma generate

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"]
EXPOSE 9090
