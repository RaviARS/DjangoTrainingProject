from celery import shared_task
import random, string


@shared_task
def celery_task(msg):
    """ To generate 4 Character OTP     """

    size = 4
    otp = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(size)])
    return 'OTP {}'.format(otp)