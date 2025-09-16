FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

COPY ./source /app

RUN pip install --no-cache-dir flask

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_SECRET_KEY=test
ENV FLAG=CTF{test}

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]

CMD ["flask", "run"]
