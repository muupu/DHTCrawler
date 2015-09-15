# -*- coding:utf-8 -*-
import dht_node

def process_message(crawler, msg, address):
    # print('Received from %s:%s.\n' % address, msg)
    if b'y' in msg:
        if msg[b'y'] == b'r':
            process_response(crawler, msg, address)
        elif msg[b'y'] == b'q':
            process_request(crawler, msg, address)

def process_response(crawler, msg, address):
    if msg[b"r"].has_key(b"nodes"):
        process_find_node_response(crawler,msg, address)

def process_find_node_response(crawler, msg, address):
    bnodes = msg[b'r'][b'nodes']
    nodes = dht_node.decode_nodes(bnodes)
    for node in nodes:
        if node.nid == crawler.crawler_nid:
            continue
        crawler.nodes.append(dht_node.Node(node.nid, node.ip, node.port))


def process_request(crawler, msg, address):
    pass


