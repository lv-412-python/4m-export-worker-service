# 4m-export-worker-service
# Worker for export service 
## Description
This is the source code of the worker for export service, part of 4m project. This service creates and sends file to user email.

## Technologies
* Python (3.6.8)
* Flask (1.0.3)
* PostgreSQL (10.8)
* RabbitMQ (3.6.10)

## Install
For the next steps of service installation, you will need setup of Ubuntu 18.04

### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
```


### In the project root create venv and install requirements with Make

```
export PYTHONPATH=$PYTHONPATH:/home/.../.../4m-export-worker-service/worker
```
```
make dev-env
```
#### in case of failure:
```
. venv/bin/activate
pip install -r requirements.txt
```

### Run project
```
export FLASK_APP=setup.py
flask run --port 7777
python create_file/create_files.py
python send_email/listen_queue.py
```



## Project team:
* **Lv-412.WebUI/Python team**:
    - @sikyrynskiy
    - @olya_petryshyn
    - @taraskonchak
    - @OlyaKh00
    - @ement06
    - @iPavliv
    - @Anastasia_Siromska
    - @romichh