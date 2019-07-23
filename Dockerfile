FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH_TO_EXPORT_FILES=/home/taras/services/export_worker_service/export_workers/files_to_export

ENV RABBITMQ_HOST=172.17.0.2
ENV RABBITMQ_PORT=5672

ENV PYTHONPATH "${PYTHONPATH}:/export_worker_service"

RUN apt update -y && \
    apt install -y python3 python3-dev python3-pip libssl-dev libffi-dev

COPY ./ ./opt/export_worker_service
WORKDIR /opt/export_worker_service

RUN pip3 install -r requirements.txt
RUN chmod a+x run_workers.sh

CMD ["./run_workers.sh"]
