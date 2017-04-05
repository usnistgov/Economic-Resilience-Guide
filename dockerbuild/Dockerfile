# docker run volume

# Sets up initial container file
FROM continuumio/miniconda3:4.3.11

WORKDIR ./media/sf_Economic-Resilience-Guide
MAINTAINER shannon.grubb@nist.gov

# Update
RUN apt-get update && \
    apt-get install -yq build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists*

COPY ./requirements-conda.txt .

RUN conda install -y python=3.6.1\
 && conda install -y --file requirements-conda.txt \
 && conda clean --all -y

CMD ls

ADD . /media/sf_Economic-Resilience-Guide
ADD . .

# Runs the code
CMD ["python", "EconGuide.py"]
