FROM python:3.8-alpine

RUN apk update
## install dependencies
RUN apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev
COPY ./requirements.txt /server/
WORKDIR /server/
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9090
CMD ["python3", "main.py"]
