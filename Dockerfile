FROM python:3.7-alpine
MAINTAINER Marcus Gunn

# Tells python to run in unbuffered mode which is recomended when running python in Docker containers
# It doesn't allow python to buffer the outputs, it just prints them directly
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create the /app directory, change location to the directory, and then copy the local machine's app folder into the docker image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create the user named user. This user will run processes only
RUN adduser -D user
# switch to the new user inside the docker image. If we do not do this, then the default user is the root user
# this is not recommended, because if the application becomes comprimised, then the attacker would have root access
USER user