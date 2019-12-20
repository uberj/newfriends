import unittest
import base64

from util.somecode import *


class TestChallenge1(unittest.TestCase):
    def test_b64_to_hex(self):
        hex_ = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        b64 = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        decoded = base64.b64decode(b64)
        self.assertEqual(BA(decoded).hex, hex_)

if __name__ == '__mai__':
    unittest.main()
