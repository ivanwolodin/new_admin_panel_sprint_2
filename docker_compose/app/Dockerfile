FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt . 

RUN pip install --upgrade pip && \ 
pip install -r requirements.txt && \
apt-get update && \
apt-get -y install postgresql-client 

COPY . .
RUN python manage.py collectstatic --clear --noinput && \
chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
