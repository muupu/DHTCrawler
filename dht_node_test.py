import unittest
import dht_node

class TestDhtNode(unittest.TestCase):
    def test_decode_nodes(self):
        compact_nodes = b'12345678901234567890ABCDFF09876543210987654321DCBAFF'
        correct_nodes = [(b'12345678901234567890', '65.66.67.68', 17990),(b'09876543210987654321', '68.67.66.65', 17990)]
        self.assertEqual(correct_nodes, dht_node.decode_nodes(compact_nodes))


if __name__ == '__main__':
    unittest.main()