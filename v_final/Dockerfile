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
RUN apt-get install -yqq curl wget vim procps
RUN apt-get install -yqq python3 python3-pip python-pip python3-tk

# SET WORKING DIRECTORY
WORKDIR $APPLICATION_PATH

# INSTALL PYTHON PACKAGES FROM requirements.txt
RUN pip3 install virtualenv && \
    python3 -m virtualenv env


RUN $APPLICATION_PATH/env/bin/pip3 install -r requirements.txt

# EXPOSE PORTS (OPTIONAL)
EXPOSE 8081

# START THE APPLICATION
ENTRYPOINT sh lauch_interface.sh

#  docker build -t test_n_puzzle .

# docker run -d -p 8081:8080 test_n_puzzle --name puzzle_docker

# docker exec -it  puzzle_docker  bash
