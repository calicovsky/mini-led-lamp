import logging
import threading
import time
import datetime

turn_off_function = None

class TurnOffTimer:

    # Used to set a function to call for turning off the light.
    turn_off = None

    # @classmethod
    # def set_turn_off_method(cls,method):
    #     cls.turn_off = method

    #     global turn_off_function
    #     turn_off_function = method

    @staticmethod
    def set_turn_off_method(method):
        TurnOffTimer.turn_off = method

    def __init__(self):
        # self.event = None
        # self.scheduler = sched.scheduler(time.time, time.sleep)
        self.timer = None

        self.hour = -1
        self.minute = -1

    def set_timer(self, hour, minute):
        # if self.event is not None:
            # self.scheduler.cancel(self.event)
            # self.event = None

        self.cancel_timer()

        if 0 <= hour and 0 <= minute:
            self.hour = hour
            self.minute = minute
        else:
            logging.info(f'Setting the timer using the current time: {self.hour}:{self.minute}')

        if self.hour < 0 or self.minute < 0:
            logging.info(f'!!! {self.hour}:{self.minute}')
            return

        # Local time offset (in hours)
        utc_offset = -9.0

        # utc_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        # t = datetime.datetime.strptime(f'{utc_date} {hour}:{min}', '%Y-%m-%d %H:%M')
        # local_time = time.localtime()
        utctime = datetime.datetime.utcnow()

        #pending_today = (local_time.tm_hour < t.hour) or (local_time.tm_hour == hour and local_time.tm_min < min)
        #offset = 0 if pending_today else 24

        h = (hour + utc_offset + 24) % 24
        seconds_to_wait = (h * 3600 + minute * 60) - (utctime.hour * 3600 + utctime.minute * 60)
        if seconds_to_wait <= 0:
            seconds_to_wait += 24 * 3600

        # self.event = self.scheduler.enter(t,1,self.turn_off)
        logging.info(f'{h}:{minute} (current {utctime.hour}:{utctime.minute})')
        logging.info(f'seconds_to_wait: {seconds_to_wait}')
        # self.timer = threading.Timer(seconds_to_wait, self.turn_off)
        self.timer = threading.Timer(seconds_to_wait, TurnOffTimer.turn_off)
        self.timer.start()

    def cancel_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

class TurnOffTimerUtil:
    # timers = []
    timers = [None]

    @classmethod
    def get_timers(cls):
        res = []
        for timer in cls.timers:
            if timer is None:
                res.append({'enabled': False})
            else:
                res.append({'enabled': True, 'hour': timer.hour, 'minute': timer.minute})
        return res

    @classmethod
    def set_timer(cls, timer_index, hour, minute):
        for i in range(len(cls.timers), timer_index+1):
            cls.timers.append(None)

        cls.timers[timer_index] = TurnOffTimer()
        cls.timers[timer_index].set_timer(hour, minute)

    @classmethod
    def clear_timer(cls, timer_index):
        if timer_index < len(cls.timers):
            timer = cls.timers[timer_index]
            if timer is None:
                logging.info(f'Timer[{timer_index}] is already canceled. Nothing to do')
            else:
                logging.info(f'Canceling the timer {timer_index}')
                timer.cancel_timer()
                cls.timers[timer_index] = None
        else:
            logging.info(f'Index value {timer_index} is not valid')

    @classmethod
    def add_timer(cls):
        cls.timers.append(None)

    @classmethod
    def remove_timer(cls, timer_index):
        logging.info(f'Removing timer {timer_index}')
        clear_timer(timer_index)
        cls.timers.pop(timer_index)