from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from catalog.scheduler.tasks import fill_requests, generate_report

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fill_requests, 'interval', minutes=10)
    scheduler.add_job(generate_report, 'interval', minutes=10)
    # scheduler.add_job(fill_requests, 'cron', hour=8) # To test, use: scheduler.add_job(fill_requests, 'interval', minutes=1)
    # scheduler.add_job(generate_report,'cron',hour=8)
    scheduler.start()