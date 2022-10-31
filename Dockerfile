FROM python:3.10-buster as base

RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/

WORKDIR /app
RUN pip install --upgrade pip==22.0.4 setuptools==61.3.1 wheel==0.37.1
RUN pip install -r requirements.txt

COPY . /app/
RUN pip install gunicorn==20.1.0
CMD bash -c "gunicorn --bind 0.0.0.0:5000 main:app --workers 2"
