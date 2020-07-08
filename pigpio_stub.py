# Stub for pigpio
# Used this for testing the app on a Linux computer
# before deploying to a pi

class PiGpioStub:

    def __init__(self):
        self.s = 'This is a stub.'

    def set_PWM_dutycycle(self, user_gpio, dutycycle):
        pass

    def set_PWM_frequency(self, user_gpio, frequency):
        pass

    def stop(self):
        pass

def pi(hostname='somehost'):
    return PiGpioStub()
