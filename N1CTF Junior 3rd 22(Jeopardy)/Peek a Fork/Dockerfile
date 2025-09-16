FROM python:3.12-slim

WORKDIR /app

COPY server.py /app/server.py
COPY entrypoint.sh /app/entrypoint.sh

RUN useradd -m ctf \
    && chown -R ctf:ctf /app \
    && chmod +x /app/entrypoint.sh

USER ctf

EXPOSE 1337

ENV FLAG=flag{test}

ENTRYPOINT ["/app/entrypoint.sh"]
