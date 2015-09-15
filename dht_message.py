# -*- coding:utf-8 -*-


def process_message(msg, address):
    # print('Received from %s:%s.\n' % address, msg)
    if b'y' in msg:
        if msg[b'y'] == b'r':
            process_response(msg, address)
        elif msg[b'y'] == b'q':
            process_request(msg, address)

def process_response(msg, address):
    if msg[b"r"].has_key(b"nodes"):
        process_find_node_response(msg, address)

def process_find_node_response(msg, address):
    pass

def process_request(msg, address):
    pass


