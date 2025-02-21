# syntax=docker/dockerfile:1
FROM ghcr.io/osgeo/gdal:ubuntu-full-latest AS base
# alternative if small docker image does not work:
# FROM ghcr.io/osgeo/gdal:ubuntu-full-latest AS base
WORKDIR /app

RUN apt-get update --fix-missing
RUN apt-get install --fix-missing -y python3-pip python3.12-venv 

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Copy the requirements.txt file into the container
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

WORKDIR /src
CMD ["jupyter" , "lab", "--allow-root", "--port=9999", "--ip=0.0.0.0", "--no-browser"]