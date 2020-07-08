from PiGPIO import PiGPIO
from threading import Thread
from datetime import datetime
#import atexit
import time
import logging

class LEDBrightnessController:

    def __init__(self):
        self.pins = [12, 16, 25, 26]
        self.pwm_frequency = 250
        for pin in self.pins:
            PiGPIO.get_pi_instance().set_PWM_frequency(pin, self.pwm_frequency)
        self.current_brightness = 0
        self.current_dc = 0

        # PiGPIO.get_pi_instance() will invoke PiGPIO's init function,
        # in which pigpio release function is registered with atexit.register().
        # atexit function registered here is called before the PiGPIO's release
        # function
#        atexit.register(self.on_exit)

    def on_exit(self):
        logging.info('Turning off LEDs')
        for pin in self.pins:
            PiGPIO.get_pi_instance().write(pin,0)

    # dc (duty cycle): [0,100]
    def set_dc(self, dc):
        if self.current_dc != dc:
            logging.info(f'Changing duty cycle from {self.current_dc} to {dc}')
            # print(f'Date and time: {datetime.now()}')
            scaled_dc = max(0, min(255, int(dc * 255 / 100)))
            logging.info(f'Scaled DC value: {scaled_dc}')
            for pin in self.pins:
                PiGPIO.get_pi_instance().set_PWM_dutycycle(pin, scaled_dc)
            self.current_dc = dc
        else:
            logging.info('Current DC == requested dc. Nothing to do.')

    # brightness: [0,100]
    def set_brightness(self, brightness):
        max_dc_at_max_brightness = 80
        max_brightness = 100

        b = max(0, min(max_brightness, brightness))
        if b == 0:
            for pin in self.pins:
                PiGPIO.get_pi_instance().write(pin,0)
        else:
            for pin in self.pins:
                PiGPIO.get_pi_instance().write(pin,1)

        self.current_brightness = b
        dc = float(b) * float(max_dc_at_max_brightness) / 100.0
        self.set_dc(int(dc))

    def get_brightness(self):
        return self.current_brightness

    def mainloop(self):
        while(True):
            t = datetime.now()
            h = t.hour
            if 19 <= h and h < 22:
                # 7p to 10p: use ceiling light
                self.set_brightness(0)
            elif 22 <= h and h < 23:
                # Starting at 10p, turn off the ceiling light and switch to this raspberry pi-powered LED lamp
                self.set_brightness(95)
            elif 0 <= h and h < 1:
                self.set_brightness(90)
            elif 1 <= h and h < 2:
                self.set_brightness(75)
            elif 2 <= h and h < 3:
                self.set_brightness(50)
            elif 2 <= h and h < 3:
                self.set_brightness(30)
            else:
                self.set_brightness(0)

            time.sleep(5)

    def run(self):
        try:
            self.mainloop()
        except:
            logging.info('Releasing pigpio')
            PiGPIO.release()

led_brightness_controller = LEDBrightnessController()

enable_auto_mode = False
if enable_auto_mode:
    thread = Thread(target=led_brightness_controller.run)
    # Start the thread (this invokes run() function of the LEDBrightnessController class)
    thread.start()

def set_brightness(brightness):
    led_brightness_controller.set_brightness(brightness)

def get_brightness():
    return led_brightness_controller.get_brightness()
