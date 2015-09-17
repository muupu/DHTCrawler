import unittest
import dht_node

class TestDhtNode(unittest.TestCase):
    def test_decode_nodes(self):
        compact_nodes = b'12345678901234567890ABCDFF09876543210987654321DCBAFF'
        correct_nodes = [dht_node.Node(b'12345678901234567890', '65.66.67.68', 17990),dht_node.Node(b'09876543210987654321', '68.67.66.65', 17990)]
        nodes = dht_node.decode_nodes(compact_nodes)
        self.assertEqual(len(correct_nodes), len(nodes))
        for correct_node in correct_nodes:
            node = nodes.popleft()
            self.assertEqual(correct_node.nid, node.nid)
            self.assertEqual(correct_node.ip, node.ip)
            self.assertEqual(correct_node.port, node.port)

    def test_encode_nodes(self):
        nodes = [dht_node.Node(b'12345678901234567890', '65.66.67.68', 17990), dht_node.Node(b'09876543210987654321', '68.67.66.65', 17990)]
        compact_nodes = b'12345678901234567890ABCDFF09876543210987654321DCBAFF'
        self.assertEqual(compact_nodes, dht_node.encode_nodes(nodes))

if __name__ == '__main__':
    unittest.main()
