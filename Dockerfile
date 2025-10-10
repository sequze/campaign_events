FROM python:3.13

RUN pip install poetry --upgrade pip wheel

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY . .

WORKDIR /app

RUN chmod a+x /docker/*

CMD ["python", "main.py"]