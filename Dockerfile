# pull official base image
FROM python:3.9.5
# set work directory
WORKDIR /usr/src/app
# install dependencies

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN sudo apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y netcat

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]