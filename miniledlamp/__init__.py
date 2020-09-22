from flask import Flask
import datetime
import logging
from PiGPIO import PiGPIO
from miniledlamp import led_brightness_controller
from miniledlamp import turn_off_timer

log_format = '%(asctime)-15s %(thread)d %(message)s'
logging.basicConfig(
    filename=f'miniledlamp_{datetime.date.today().isoformat()}.log',
    level=logging.DEBUG,
    format=log_format)

turn_off_timer.TurnOffTimer.set_turn_off_method(led_brightness_controller.turn_off)

app = Flask(__name__)

from miniledlamp import routes