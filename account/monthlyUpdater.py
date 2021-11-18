from .job import  Credit_balanace_reset
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Credit_balanace_reset, 'interval', minutes=5 )
    scheduler.start()