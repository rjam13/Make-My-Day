# calls python image
FROM python:3.8

# environment settings
# sets python output to the terminal
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt