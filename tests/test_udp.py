from pyjama import udp
import unittest

class TestEncoding(unittest.TestCase):

    def setUp(self):
        self.obj = {"a": "object"}

    def tearDown(self):
        pass

    def test_cycle(self):
        assert self.obj == udp.decode_msg(udp.encode_msg(self.obj))
