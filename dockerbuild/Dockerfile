# docker run volume

# Sets up initial container file
#FROM microsoft/nanoserver
FROM continuumio/miniconda:4.3.11

WORKDIR C:/media/sf_Economic-Resilience-Guide
MAINTAINER shannon.grubb@nist.gov

# Update
RUN apt-get update python py-pip && \
    apt-get install -yq build-essential && \
   apt-get clean && \
    rm -rf /var/lib/apt/lists*

COPY ./requirements-conda.txt .

RUN conda install -y python=3.6.1\
 && conda install -y --file requirements-conda.txt \
 && conda clean --all -y


# Install app dependencies
#RUN pip install numpy
#RUN pip install matplotlib

# Runs the code
CMD ["python", "EconGuide.py"]
