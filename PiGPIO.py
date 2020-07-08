import logging
import socket
import subprocess
#import atexit

def is_running_on_raspberry_pi():
    stdout = subprocess.check_output(['ip','a']).decode('utf-8')
    pos = stdout.find('link/ether b8:27:eb')
    return (pos != -1)

if is_running_on_raspberry_pi():
    import pigpio
else:
    import pigpio_stub as pigpio

# Initializes and manages pigpio instances, assuming that
# - pigpiod is running
# - Environment variable PIGPIO_PORT is set to the port
#   pigpiod is running on if the port is a non-standard one

class PiGPIO:

    pi = None

    @classmethod
    def init(cls):
        logging.info('Initializing pigpio.')

        #cls.pi = pigpio.pi() # Connect to local pi

        # Once pigpio.pi() on a machine via ssh caused an error
        # and hostname had to be specified. Later executions
        # of the script in the same environment did not cause the error
        # and reasons for this discrepancy was not resolved.
        cls.pi = pigpio.pi(socket.gethostname()) # Connect to local pi

        #atexit.register(PiGPIO.release)

    @classmethod
    def get_pi_instance(cls):
        if cls.pi is None:
            cls.init()

        return cls.pi

    @classmethod
    def release(cls):
        if cls.pi is not None:
            logging.info('Releasing pigpio resources.')
            cls.pi.stop()
            cls.pi = None
