# -*- coding:utf-8 -*-
import dht_node
from bencode import bencode
import dht_id

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
    # print('find node response')
    bnodes = msg[b'r'][b'nodes']
    nodes = dht_node.decode_nodes(bnodes)
    for node in nodes:
        if node.nid == crawler.crawler_nid:
            continue
        # crawler.nodes.append(dht_node.Node(node.nid, node.ip, node.port))
        crawler.nodes.add(node)


def process_request(crawler, msg, address):
    if b'q' in msg:
        if msg[b'q'] == b'ping':
            print('ping request')
            process_ping_request(crawler, msg, address)
        elif msg[b'q'] == b'find_node':
            print('find_node request')
            process_find_node_request(crawler, msg, address)
        elif msg[b'q'] == b'get_peers':
            print('get_peers request')
            process_get_peers_request(crawler, msg, address)
        elif msg[b'q'] == b'announce_peer':
            print('announce_peer request')
            announce_peer_request(crawler, msg, address)


def send_response(socket, address, response):
    bresponse = bencode(response)
    send_message(socket, address, bresponse)


def send_message(socket, address, msg):
    socket.sendto(msg, address)


def process_find_node_request(crawler, msg, address):
    # 加入nodes
    crawler.nodes.add(dht_node.Node(nid=msg[b'a'][b'id'], ip=address[0], port=address[1]))
    # print(address[0], address[1])
    # 最近8个邻居节点信息
    close_nodes = crawler.nodes.get_close_nodes()
    # 发送response
    response = {
        't': msg[b't'],
        'y':'r',
        'r':{
            'id':crawler.crawler_nid,
            'nodes':dht_node.encode_nodes(close_nodes)
        }
    }
    send_response(crawler.sock, address, response)


def process_ping_request(crawler, msg, address):
    # 加入nodes
    crawler.nodes.add(dht_node.Node(msg[b'a'][b'id'], address[0], address[1]))
    response = {
        't':msg[b't'],
        'y':'r',
        'r':{'id':crawler.crawler_nid}
    }
    send_response(crawler.sock, address, response)


def process_get_peers_request(crawler, msg, address):
    # 加入nodes
    crawler.nodes.add(dht_node.Node(nid=msg[b'a'][b'id'], ip=address[0], port=address[1]))
    # 最近8个邻居节点信息
    close_nodes = crawler.nodes.get_close_nodes()
    # 发送response
    response = {
        't': msg[b't'],
        'y':'r',
        'r':{
            'id':crawler.crawler_nid,
            'token':dht_id.gen_random_nid(),
            'nodes':dht_node.encode_nodes(close_nodes)
        }
    }
    send_response(crawler.sock, address, response)


def announce_peer_request(crawler, msg, address):
    crawler.nodes.add(dht_node.Node(nid=msg[b'a'][b'id'], ip=address[0], port=address[1]))
    print(msg[b'a'][b'info_hash'])