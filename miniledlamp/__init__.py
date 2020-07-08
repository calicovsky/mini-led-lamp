from flask import Flask
import datetime
import logging
from PiGPIO import PiGPIO

log_format = '%(asctime)-15s %(thread)d %(message)s'
logging.basicConfig(
    filename=f'miniledlamp_{datetime.date.today().isoformat()}.log',
    level=logging.DEBUG,
    format=log_format)

app = Flask(__name__)

from miniledlamp import routes