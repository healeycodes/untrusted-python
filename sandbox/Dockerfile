FROM python:3.10-bookworm

RUN apt-get update -y
RUN apt-get install -y libseccomp-dev
RUN apt-get install -y strace

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV GUNICORN_CMD="gunicorn -w 4 -b 0.0.0.0:3000"
EXPOSE 3000
CMD ["/bin/bash", "-c", "$GUNICORN_CMD api:app"]
