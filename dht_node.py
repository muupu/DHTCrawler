# -*- coding:utf-8 -*-
import socket
import struct
from collections import deque

def decode_nodes(compact_nodes):
    nodes = []
    length = len(compact_nodes)
    if (length % 26) != 0:
        return nodes
    for i in range(0, length, 26):
        node_id = compact_nodes[i:i+20]
        node_ip = socket.inet_ntoa(compact_nodes[i+20:i+24])
        node_port = struct.unpack("!H", compact_nodes[i+24:i+26])[0]
        nodes.append(Node(node_id, node_ip, node_port))
    return nodes

def encode_nodes(nodes):
    compact_nodes = b''
    for node in nodes:
        compact_nodes += node.nid
        compact_nodes += socket.inet_aton(node.ip)
        compact_nodes += struct.pack("!H", node.port)
    return compact_nodes

class Node:

    def __init__(self, node_id, node_ip, node_port):
        self.nid = node_id
        self.ip = node_ip
        self.port = node_port


class Nodes:

    def __init__(self, max_node_qsize):
        self.max_node_qsize = max_node_qsize
        self.nodes = deque(maxlen=max_node_qsize)

    def add(self, nodes):
        self.nodes.extend(nodes)

    def pop(self):
        return self.nodes.popleft()

    def get_close_nodes(self):
        return self.nodes[:8]
