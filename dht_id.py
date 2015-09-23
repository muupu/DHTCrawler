# -*- coding:utf-8 -*-
from random import randint
from hashlib import sha1

def gen_tid():
    return ''.join(chr(randint(0, 127)) for _ in range(2))

def gen_random_nid():
    # h = sha1()
    # e = ''.join(chr(randint(0, 127)) for _ in range(20)).encode('utf-8')
    # h.update(e)
    # return h.digest()
    return ''.join(chr(randint(0, 127)) for _ in range(20))
