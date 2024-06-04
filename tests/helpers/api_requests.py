import string
import random


def generate_random_gid():
    num = 27
    res = ''.join(random.choices(string.ascii_letters + string.digits + "_", k=num))
    return 'gid:' + res
