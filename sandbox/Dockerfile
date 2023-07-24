FROM python:3.10-bookworm

RUN apt-get update -y
RUN apt-get install -y libseccomp-dev
RUN apt-get install -y strace

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV FLASK_APP=api.py
EXPOSE 3000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "3000"]
