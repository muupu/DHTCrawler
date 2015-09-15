# -*- coding:utf-8 -*-
import dht_node

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
    bnodes = msg[b'r'][b'nodes']
    nodes = dht_node.decode_nodes(bnodes)

def process_request(msg, address):
    pass


