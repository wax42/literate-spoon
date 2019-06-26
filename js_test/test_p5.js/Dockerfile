FROM debian:9


# DEFINE ENVIRONNEMENT VARIABLES
ENV APPLICATION_PATH /var/www/n_puzzle
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8

ENV PATH=$APPLICATION_PATH/env/bin:${PATH}


# CREATE FOLDERS
RUN mkdir /var/www
RUN mkdir $APPLICATION_PATH

# ADD FILE IN THE CONTAINER
ADD . $APPLICATION_PATH

# INSTALL DEPENDENCIES (Python3)
RUN apt-get -yqq update
RUN apt-get install -yqq python3 python3-pip python-pip python3-tk

# SET WORKING DIRECTORY
WORKDIR $APPLICATION_PATH

# INSTALL PYTHON PACKAGES FROM requirements.txt
RUN pip3 install virtualenv && \
    python3 -m virtualenv env
# $APPLICATION_PATH/env/bin/pip3 install -r requirements.txt

# EXPOSE PORTS (OPTIONAL)
EXPOSE 8080

# START THE APPLICATION
ENTRYPOINT python3 file_server.py && python3 tornado_websocket.py

