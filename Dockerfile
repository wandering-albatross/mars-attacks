FROM python:3
ENV \
  # do not buffer python output at all
  PYTHONUNBUFFERED=1 \
  # do not ask any interactive question
  POETRY_NO_INTERACTION=1 \
  # do not create venvs
  POETRY_VIRTUALENVS_CREATE=false \
  # do not write `__pycache__` bytecode
  PYTHONDONTWRITEBYTECODE=1

#RUN apt-get update
#RUN apt-get install -y swig libssl-dev dpkg-dev netcat

RUN pip install -U --pre pip poetry
ADD poetry.lock /code/
ADD pyproject.toml /code/
WORKDIR /code
RUN poetry install --no-interaction --no-root

COPY . /code/
