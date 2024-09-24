# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# static files
RUN mkdir /usr/src/app/staticfiles

# copy entrypoint.prod.sh
COPY ./entrypoint.sh /usr/src/app
RUN sed -i 's/\r$//g'  /usr/src/app/entrypoint.sh
RUN chmod +x  /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

