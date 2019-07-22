#!/bin/bash
PYTHONPATH="${PYTHONPATH}:/export_workers"
export PYTHONPATH
export WORKER_EMAIL_ADDRESS="4m.export.service@gmail.com"
export WORKER_EMAIL_PASSWORD="qwertyytrewq13242151"
export MAIL_SERVER="smtp.gmail.com"
export MAIL_SERVER_PORT=465
export PATH_TO_EXPORT_FILES="./export_workers/files_to_export"
export RABBITMQ_HOST=172.17.0.2
export RABBITMQ_PORT=5672
PATH_TO_CREDENTIALS="./export_workers/workers/google_drive"
source ./venv/bin/activate
export PATH_TO_CREDENTIALS
python3 ./export_workers/workers/create_file/create_files.py &
python3 ./export_workers/workers/send_email/email_listener.py &
python3 ./export_workers/workers/google_drive/google_drive_listener.py &
# python3 ./export_workers/workers/delete_files.py &
sleep infinity