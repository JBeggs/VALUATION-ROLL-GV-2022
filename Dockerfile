# Pull base image
FROM python:3.10
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

RUN apt-get update && apt-get -y install cron

COPY crontab.txt /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

RUN touch /var/log/cron.log
RUN chown www-data: /var/log/cron.log

RUN service cron start

# Install dependencies
COPY ./requirements.txt .

RUN pip install -r requirements.txt


#copy local files
COPY . . 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]
