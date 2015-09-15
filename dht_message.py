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
    if b"nodes" in msg[b"r"]:
        process_find_node_response(crawler,msg, address)

def process_find_node_response(crawler, msg, address):
    print('find node response')
    bnodes = msg[b'r'][b'nodes']
    nodes = dht_node.decode_nodes(bnodes)
    for node in nodes:
        if node.nid == crawler.crawler_nid:
            continue
        # crawler.nodes.append(dht_node.Node(node.nid, node.ip, node.port))
        crawler.nodes.put(node)


def process_request(crawler, msg, address):
    if b'q' in msg:
        if msg[b'q'] == b'ping':
            print('ping request')
        elif msg[b'q'] == b'find_node':
            print('find_node request')
        elif msg[b'q'] == b'get_peers':
            print('get_peers request')
        elif msg[b'q'] == b'announce_peer':
            print('announce_peer request')



