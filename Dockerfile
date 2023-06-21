# Dockerfile
FROM python:3.10.0a7-slim-buster
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pipx
RUN pip install -r requirements.txt
RUN alembic upgrade head

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
