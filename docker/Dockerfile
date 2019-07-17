#####################################################
# Dockerfile to build PICOSS interface container
# Based on Ubuntu
####################################################

FROM ubuntu:14.04
MAINTAINER Angel Bueno
LABEL com.example.version="0.1"

#####################################################
# INITIAL SETTING
####################################################
RUN \
  apt-get update && \
  apt-get install -y pkg-config python python-dev python-pip && \
  apt-get install -y libfreetype6-dev libpng12-dev  && \
  apt-get install -y libxml2-dev libxslt1-dev && \
  apt-get install -y python-lxml && \
  apt-get install -y \ 
			python-numpy \
			python-scipy \
			python-nose \
			python-h5py \
			python-matplotlib \
			python-sklearn \ 
			&& \
  apt-get install -y python-qt4 qt4-dev-tools && \
  rm -rf /var/lib/apt/lists/*

# Define working directory.
COPY requirements.txt /home/picos/requirements.txt
WORKDIR /home/picos
RUN pip install -r requirements.txt


#copy the rest of the application
COPY menus/ /home/picos/menus
COPY picos.py /home/picos
COPY run_picos.py /home/picos

# Define data volume to store the segmented data and avoid future losses:

VOLUME /home/picos/data
VOLUME /home/picos/segmented_data

# Define default command.
CMD ["python", "run_picos.py"]


