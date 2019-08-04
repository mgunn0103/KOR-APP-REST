FROM python:3.7-alpine
MAINTAINER Marcus Gunn

# Tells python to run in unbuffered mode which is recomended when running python in Docker containers
# It doesn't allow python to buffer the outputs, it just prints them directly
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
# uses the apk package manager that comes with Alpine  
# the "add" command tells it that we are going to add a package
# "--update" means update the registry before we add it 
# "no-cache" means don't store the registry index on our DockerFile
# this allows us to minimize the number of extra files and containers that 
# are included in our docker container to keeep the docker footprint as small as possible
# it also means that you dont include extra dependencies or anything on your system which may 
# cause unexpected side effects or even security vulnerabilities  
RUN apk add --update --no-cache postgresql-client

# next we are going to install some temporary packages that need to be on the system while we install 
# our requirements. We can then remove them after our requirements have run
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# now we can remove the temporary packages now that they are no longer needed
RUN apk del .tmp-build-deps

# create the /app directory, change location to the directory, and then copy the local machine's app folder into the docker image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create the user named user. This user will run processes only
RUN adduser -D user
# switch to the new user inside the docker image. If we do not do this, then the default user is the root user
# this is not recommended, because if the application becomes comprimised, then the attacker would have root access
USER user