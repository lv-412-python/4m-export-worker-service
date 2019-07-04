"""Module deletes old files"""
import atexit
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

PATH = os.path.dirname(os.path.abspath(__file__)) + '/files_to_export'

def delete_files():
    """Deletes files that were creaded more than 15 minutes ago"""
    files = os.listdir(PATH)
    now = time.time()
    for file in files:
        file = os.path.join(PATH, file)
        if os.stat(file).st_mtime < now - 15 * 60:
            os.remove(file)


SCHEDULER = BackgroundScheduler(daemon=True)
SCHEDULER.add_job(func=delete_files, trigger="interval", minutes=1)
SCHEDULER.start()

def stop_deleting():
    """stops deleting"""
    SCHEDULER.shutdown()


atexit.register(stop_deleting)
