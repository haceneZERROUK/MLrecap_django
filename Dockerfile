FROM python:3.11-slim

WORKDIR /django_app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    gnupg \
    python3-dev \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install --upgrade pip
COPY requirements.txt /django_app/
RUN pip3 install -r requirements.txt
    
RUN mkdir -p /django_app/niab/static/css \
    && mkdir -p /django_app/niab/static/images \
    && mkdir -p /django_app/niab/staticfiles

COPY niab/static /django_app/niab/static/

COPY .env /django_app/
COPY . /django_app

COPY entrypoint.sh /django_app/entrypoint.sh
COPY data_load_save.py /django_app/data_load_save.py
COPY upcomes.json /django_app/upcomes.json

RUN chmod +x /django_app/entrypoint.sh

EXPOSE 8800

ENTRYPOINT ["/django_app/entrypoint.sh"]




