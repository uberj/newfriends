import unittest

from util.somecode import *
from binascii import a2b_hex


class TestChallenge2(unittest.TestCase):
    def test_simple_zeros(self):
        hex_ = a2b_hex("0000")
        xorv = a2b_hex("ffff")
        expected = a2b_hex("ffff")

        l = xor(hex_, xorv)
        self.assertEqual(l, expected)

    def test_simple_alternate2(self):
        a = a2b_hex("f0f0")
        b = a2b_hex("ffff")
        expected = a2b_hex("0f0f")

        l = xor(a, b)
        self.assertEqual(l, expected)

    def test_example1(self):
        a = a2b_hex("181c")
        b = a2b_hex("7965")
        expected = a2b_hex("6179")

        l = xor(a, b)
        self.assertEqual(l, expected)

    def test_example(self):
        a = a2b_hex("1c0111001f010100061a024b53535009181c")
        b = a2b_hex("686974207468652062756c6c277320657965")
        expected = a2b_hex("746865206b696420646f6e277420706c6179")

        l = xor(a, b)
        self.assertEqual(l, expected)
