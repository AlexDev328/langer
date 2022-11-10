FROM python:3.10-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh .


# copy project
COPY .. .
RUN chmod +x /usr/src/app/entrypoint.sh
# run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

