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
# these dependencies remain in the docker container once it is built 
RUN apk add --update --no-cache postgresql-client jpeg-dev

# next we are going to install some temporary packages that need to be on the system while we install 
# our requirements. We can then remove them after our requirements have run
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

# now we can remove the temporary packages now that they are no longer needed
RUN apk del .tmp-build-deps

# create the /app directory, change location to the directory, and then copy the local machine's app folder into the docker image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# any files that may need to be shared with other containers are stored in vol, short for "volume"
# this way we know where all of the volume mappings need to be in our container if we need to share data
# with other containers in our service. 
# For example, if you had a nginx or a web server that needed to serve these media files, you know that you would need to
# map this volume and share it with the web server container
# the media directory is typically used for any media files that are uploaded by the user
# "-p" means make all of the subdirectories including the directory that we need
RUN mkdir -p /vol/web/media

# In Django, you typically have two files that hold static data. One is the 'static', and that is typically used for things
# like Javascript or any static text files, things that are not typicaly changing during the execution of the application
RUN mkdir -p /vol/web/static

# create the user named user. This user will run processes only
RUN adduser -D user

# change the ownership of the files that we created to be the user that we just created. 
# It is important that this is done before we switch to the user because it cannot give itself permissions to view
# "-R" means recursive
RUN chown -R user:user /vol

# Add the permissions
# the owner can do eveything
# everyone else can read and execute
RUN chmod -R 755 /vol/web

# switch to the new user inside the docker image. If we do not do this, then the default user is the root user
# this is not recommended, because if the application becomes comprimised, then the attacker would have root access
USER user