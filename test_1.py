import unittest
import base64

from thecode import *


class Test64(unittest.TestCase):

    def test_tb_to_octets1(self):
        h = int("010011010110000101101110", 2)
        self.assertEqual(int_to_sextet(h), [19, 22, 5, 46])

    def test_hex_to_triple_bytes1(self):
        h = "4d"
        self.assertEqual(hex_to_ints(h), [77])

    def test_hex_to_triple_bytes2(self):
        h = "4d616e"
        f = "4d616d"
        e = "000000"
        self.assertEqual(hex_to_ints(h), [5071214])
        self.assertEqual(hex_to_ints(h+f+e), [5071214, 5071213, 0])

    def test_wikipedia_example(self):
        hex = "4d616e"
        expected = "TWFu"
        self.assertEqual(hex_to_base64(hex), expected, "Should be " + expected)

    def test_example(self):
        hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        self.assertEqual(hex_to_base64(hex), expected, "Should be " + expected)

    def test_example_with_library(self):
	    pass
        # hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        # expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        # base64.b44
        # self.assertEqual(base64.b64encode(hex), expected, "Should be " + expected)

if __name__ == '__mai__':
    unittest.main()
