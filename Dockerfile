FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV SERVICES_PORT=5050

# RUN apk add --no-cache tzdata
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update -y && \
    apt install -y python3 python3-dev python3-pip libssl-dev libffi-dev

COPY ./ ./opt/export_worker_service
WORKDIR /opt/export_worker_service

RUN pip3 install -r requirements.txt
RUN chmod a+x run_workers.sh

CMD ["./run_workers.sh"]
