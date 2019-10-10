FROM python:3.7.4-alpine3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apk update && apk add wkhtmltopdf postgresql-dev gcc python3-dev musl-dev && rm -rf /var/cache/apk
RUN pip install -r requirements.txt
