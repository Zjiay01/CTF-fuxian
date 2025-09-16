FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN mv flag /flag

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install flask

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y iputils-ping

RUN chmod +x ./start.sh

CMD ["./start.sh"]