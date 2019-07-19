"""Module deletes old files"""
import atexit
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler

PATH_TO_EXPORT_FILES = os.environ.get('PATH_TO_EXPORT_FILES')


def delete_files():
    """Deletes files that were created more than 15 minutes ago"""
    files = os.listdir(PATH_TO_EXPORT_FILES)
    now = time.time()
    for file in files:
        file = os.path.join(PATH_TO_EXPORT_FILES, file)
        if os.stat(file).st_mtime < now - 15 * 60:
            os.remove(file)


SCHEDULER = BackgroundScheduler(daemon=True)
SCHEDULER.add_job(func=delete_files, trigger="interval", minutes=1)
SCHEDULER.start()


def stop_deleting():
    """stops deleting"""
    SCHEDULER.shutdown()


atexit.register(stop_deleting)
