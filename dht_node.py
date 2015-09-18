# -*- coding:utf-8 -*-
import socket
import struct
from collections import deque

def decode_nodes(compact_nodes):
    nodes = Nodes()
    length = len(compact_nodes)
    if (length % 26) != 0:
        return nodes
    for i in range(0, length, 26):
        node_id = compact_nodes[i:i+20]
        node_ip = socket.inet_ntoa(compact_nodes[i+20:i+24])
        node_port = struct.unpack("!H", compact_nodes[i+24:i+26])[0]
        nodes.add(Node(node_id, node_ip, node_port))
    return nodes

def encode_nodes(nodes):
    compact_nodes = b''
    for node in nodes:
        compact_nodes += node.nid
        compact_nodes += socket.inet_aton(node.ip)
        compact_nodes += struct.pack("!H", node.port)
    return compact_nodes

class Node:

    def __init__(self, nid=None, ip, port):
        self.nid = nid
        self.ip = ip
        self.port = port


class Nodes:

    def __init__(self, max_node_qsize = 500):
        self.max_node_qsize = max_node_qsize
        self.nodes = deque(maxlen=max_node_qsize)

    def __len__(self):
        return len(self.nodes)

    def add(self, node):
        self.nodes.append(node)

    def adds(self, nodes):
        self.nodes.extend(nodes)

    def pop(self):
        return self.nodes.pop()

    def popleft(self):
        return self.nodes.popleft()

    def get_close_nodes(self):
        return self.nodes[:8]
