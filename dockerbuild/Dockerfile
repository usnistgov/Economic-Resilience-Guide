# Sets up initial container file
#FROM microsoft/nanoserver
FROM alpine:3.1

WORKDIR C:/media/sf_Economic-Resilience-Guide
MAINTAINER shannon.grubb@nist.gov

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install numpy
RUN pip install matplotlib

# Runs the code
CMD ["python", "EconGuide.py"]
