#define base container
ARG BASE_CONTAINER=jupyter/scipy-notebook:04f7f60d34a6
FROM $BASE_CONTAINER
#create some metadata for the image
LABEL maintainer = "Nate Damen <nate.damen@gmail.com>" \
      version="0.1" \
      description = " Notebooks and data for creating tensorflowlite model of arm gesture recognition from Accl and Gyro data"

#make a working directory
WORKDIR /app

COPY . /app

#mount point
VOLUME /app/data

#expose the port
EXPOSE 8888

USER root
RUN apt-get update && apt-get -qq install xxd

#install tensorflow 2.2
RUN pip install --quiet --no-cache-dir \
    'tensorflow==2.2.0' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

#run notebook upon container launch
CMD ["jupyter","notebook","--ip='*'","--port=8888","--no-browser","--allow-root","--password=password"]

#to build the docker file, cd to the appropriate directory and copy past the following into the terminal: docker build -t atltvhead/gesture_bracer . 
#to run the this docker file use the following:  docker run -e PASSWORD=password -p 10000:8888 -v "C:/Users/nated/Documents/Python Scripts/Atltvhead-Gesture-Recognition-Bracer:/app/data" --name bracer atltvhead/gesture_bracer:latest
#to find out what the token is use the following docker exec bracer jupyter notebook list
#when restarting the docker container use http://localhost:10000/tree? to go to the notebook
#when needing to add software or access the sudo command line for the docker use the following command in a windows cmd: docker exec -it -u root bracer bash