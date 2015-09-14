# -*- coding:utf-8 -*-
from random import randint
from hashlib import sha1

def gen_tid():
    return ''.join(chr(randint(0, 255)) for _ in range(2))

def gen_random_nid():
    h = sha1()
    e = ''.join(chr(randint(0, 255)) for _ in range(20)).encode('utf-8')
    h.update(e)  # 必须加.encode('utf-8')，否则报Unicode-objects must be encoded before hashing
    return h.hexdigest()
