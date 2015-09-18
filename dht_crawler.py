# -*- coding:utf-8 -*-

import socket
from threading import Timer, Thread
from time import sleep
from queue import Queue
from bencode import bencode, bdecode
import dht_id
import dht_message
import dht_node

INIT_NODES = (
    {"ip":"router.bittorrent.com", "port":6881},
    {"ip":"dht.transmissionbt.com", "port":6881},
    {"ip":"router.utorrent.com", "port":6881}
)

class dhtcrawler(Thread):
    def __init__(self, ip, port, max_node_size):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        # self.nodes = Queue(maxsize = max_node_size)
        self.nodes = dht_node.Nodes(max_node_qsize = max_node_size)
        self.crawler_nid = dht_id.gen_random_nid()
        self.is_crawling = False
        self.join_dht_thread = Thread(target=self.join_dht)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind((self.ip, self.port))

    def run(self):
        self.is_crawling = True
        self.join_dht_thread.start()
        while self.is_crawling:
                (data, address) = self.sock.recvfrom(65536)
                msg = bdecode(data)
                dht_message.process_message(self, msg, address)

    def join_dht(self):
        while self.is_crawling:
            while len(self.nodes) > 0:
                node = self.nodes.popleft()
                self.send_find_node(node)
                sleep(0.5)
            for init_node in INIT_NODES:
                self.send_find_node(dht_node.Node(ip = init_node["ip"], port = init_node["port"]))
            sleep(3)

    def send_find_node(self, node):
        query = {
            "t" : dht_id.gen_tid(),
            "y" : "q",
            "q" : "find_node",
            "a" : {
                "id" : self.crawler_nid,
                "target" : dht_id.gen_random_nid()
            }
        }
        bquery = bencode(query)
        self.sock.sendto(bquery, (node.ip, node.port))


    def stop(self):
        self.is_crawling = False

if __name__ == "__main__":
    dht = dhtcrawler("0.0.0.0", 6881, 100)
    dht.start()