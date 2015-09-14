# -*- coding:utf-8 -*-

import socket
from threading import Timer, Thread
from queue import Queue
from bencode import bencode, bdecode
import dht_id

INIT_NODES = (
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
)

class dhtcrawler(Thread):
    def __init__(self, ip, port, max_node_size):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.nodes = Queue(maxsize = max_node_size)
        self.crawler_nid = dht_id.gen_random_nid()
        self.is_crawling = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind((self.ip, self.port))

    def run(self):
        self.is_crawling = True
        self.join_dht()
        Timer(10, self.join_dht).start()
        while self.is_crawling:
            try:
                (data, address) = self.sock.recvfrom(65536)
                msg = bdecode(data)
                self.process_message(msg, address)
            except Exception:
                pass

    def join_dht(self):
        while self.is_crawling:
            if self.nodes.qsize() == 0:
                for init_node in INIT_NODES:
                    self.find_node(init_node)
            else:
                node = self.nodes.get()
                self.find_node((node.ip, node.port))



    def find_node(self, node):
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
        self.sock.sendto(bquery, node)

    def stop(self):
        self.is_crawling = False

if __name__ == "__main__":
    dht = dhtcrawler("0.0.0.0", 6881, 100)
    dht.start()