#!.env/bin/python

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from lxml import etree as ET
import requests
from requests.auth import HTTPBasicAuth
from horizon import config


# flask app
api = Flask(__name__)
api.config["SECRET_KEY"] = config.SECRET_KEY
api.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(api)

# celery app
app = Celery(__name__,
            broker=config.CELERY_BROKER_URL,
            backend=config.CELERY_RESULT_BACKEND)

# logger
logger = get_task_logger(__name__)

#######################################################
# **********         Flask Routes          ***********#
#######################################################


@api.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        today=get_date
    )


#######################################################
# **********         Celery Tasks         *********** #
#######################################################


# set up periodic tasks
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # call every 10 seconds.
    sender.add_periodic_task(30.0, get_date, name="Log date every 30 seconds.")
    sender.add_periodic_task(30.0, test.s("Hello World!"), name='Print Hello World every 30 seconds.')
    sender.add_periodic_task(10.0, add.s(1000, 2618), name="Add numbers every 10 seconds.")
    sender.add_periodic_task(60.0, mul.s(43, 92), name="Multiply numbers every 60 seconds.")
    sender.add_periodic_task(600.0, xsum.s([12, 88, 150, 65]), name="XSum array every 10 minutes.")
    sender.add_periodic_task(
        crontab(), # empty braces denotes every minute || ex: (hour=7, minute=30, day_of_week=1)
        test.s("Celery Automation FTW!"),
        name="Print string on Crontab Schedule"
    )


@app.task
def test(arg):
    logger.critical(arg)
    return arg


@app.task
def add(x, y):
    logger.info("The sum is: {}".format(str(x + y)))
    return x + y


@app.task
def mul(x, y):
    product = x * y
    logger.info("The product is: {}".format(str(product)))
    return product


@app.task
def xsum(arrList):
    if not isinstance(arrList, list):
        arrList = list(arrlist)
    sum_total = 0
    for i in arrList:
        sum_total += i
    logger.info("XSum total is: {}".format(str(sum_total)))
    return sum_total


@app.task
def get_date():
    """
    Return the date as string 
    """
    return datetime.now().strftime("%c")


if __name__ == "__main__":
    api.start()