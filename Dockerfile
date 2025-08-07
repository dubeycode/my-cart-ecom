FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    netcat gcc postgresql-client libpq-dev && \
    apt-get clean

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

# RUN python 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
