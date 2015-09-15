# -*- coding:utf-8 -*-
import socket
import struct

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

class Node:

    def __init__(self, node_id, node_ip, node_port):
        self.nid = node_id
        self.ip = node_ip
        self.port = node_port
