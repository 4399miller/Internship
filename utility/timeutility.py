import time
from datetime import datetime, timedelta


def now():
    return datetime.now()


def utcnow():
    return datetime.utcnow()


def strf_utcnow():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def strf_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def strftime(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def isLoginPreExpire(ticks):
    exp_time = datetime.utcfromtimestamp(ticks)
    print(exp_time, utcnow())
    exp_time -= timedelta(days=2)
    if exp_time > utcnow():
        return False
    else:
        return True




