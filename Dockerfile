FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install -y build-essential libpq-dev && \
    pip install --upgrade pip && pip install -r requirements.txt && \
    apt-get remove -y build-essential && rm -rf /var/lib/apt/lists/*
COPY . /code/
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]
