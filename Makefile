.PHONY: help install clear lint dev-env prod-env
PYTHON_PATH_ANSWERS_SERVICE :=  export_worker_service-repo
PYTHON_PATH_TO_EXPORT_WORKER := export_worker_service/export_worker_service
PYTHON_PATH_TO_EXPORT_WORKER := export_worker_service/export_worker_service/workers/create_file
.DEFAULT: help
help:
	@echo "make install"
	@echo "       creates venv and installs requirements"
	@echo "make dev-env"
	@echo "       run project in dev mode"
	@echo "make prod-env"
	@echo "       run project in production mode"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make clear"
	@echo "       deletes venv and .pyc files"

install:
	python3 -m venv venv
	. venv/bin/activate; \
	pip install setuptools --upgrade; \
	pip install pip --upgrade; \
	pip install -r requirements.txt;

clear:
	rm -rf venv
	find -iname "*.pyc" -delete

dev-env:
	 . venv/bin/activate; \
	 export PYTHONPATH=$(PYTHON_PATH_ANSWERS_SERVICE); \
     export


prod-env:
	 . venv/bin/activate; \
	 export PYTHONPATH=$(PYTHON_PATH_ANSWERS_SERVICE); \
	 export PYTHONPATH=$(PYTHON_PATH_TO_EXPORT_WORKER); \
     python ./workers/create_file/create_files.py;

lint:
	. venv/bin/activate; \
	pylint setup.py answers_service/