FROM ubuntu:18.04
MAINTAINER Craig Derington
RUN apt update && apt upgrade -y
RUN apt install -y gcc python3-pip python3-dev python-pil libxml2-dev
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5580
CMD ["gunicorn", "-b", "0.0.0.0:5580", "-w", "4", "wsgi:app", "--chdir", "/app/horizon/"]


