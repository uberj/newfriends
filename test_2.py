import unittest

from set1 import *
from bitstring import BitArray as BA


class Test64(unittest.TestCase):
    def test_simple_zeros(self):
        hex = "0000"
        xorv = "ffff"
        expected = "ffff"

        buff0 = hex_to_ints(hex)
        buff1 = hex_to_ints(xorv)
        l = xor(buff0, buff1)
        self.assertEqual(ints_to_hex(l), expected, "Should be " + expected)

    def test_my_math(self):
        hex = "f"
        xorv = "f"
        expected = int("0", 16)
        self.assertEqual(expected, int(hex, 16) ^ int(xorv, 16))

        hex = "f0f0"
        xorv = "ffff"
        expected = int("0f0f", 16)
        self.assertEqual(expected, int(hex, 16) ^ int(xorv, 16))

    def test_simple_alternate1(self):
        hex = "f"
        xorv = "f"
        expected = int("0", 16)

        buff0 = hex_to_ints(hex)
        buff1 = hex_to_ints(xorv)
        l = xor(buff0, buff1)
        self.assertEqual(l[0], expected)

    def test_simple_alternate2(self):
        hex = "f0f0"
        xorv = "ffff"
        expected = "0f0f"


        buff0 = hex_to_ints(hex)
        buff1 = hex_to_ints(xorv)
        l = xor(buff0, buff1)
        h = ints_to_hex(l)
        self.assertEqual(h, expected)

    def test_example1(self):
        hex = "181c"
        xorv = "7965"
        expected = "6179"

        buff0 = hex_to_ints(hex)
        buff1 = hex_to_ints(xorv)
        l = xor(buff0, buff1)
        self.assertEqual(l[0], int(expected, 16))
        h = ints_to_hex(l)
        self.assertEqual(h, expected)

    def test_example(self):
        hex = "1c0111001f010100061a024b53535009181c"
        xorv = "686974207468652062756c6c277320657965"
        expected = "746865206b696420646f6e277420706c6179"

        buff0 = hex_to_ints(hex)
        buff1 = hex_to_ints(xorv)
        l = xor(buff0, buff1)
        self.assertEqual(ints_to_hex(l), expected, "Should be " + expected)

    def test_example_with_library(self):
        hex = BA("0x1c0111001f010100061a024b53535009181c")
        xorv = BA("0x686974207468652062756c6c277320657965")
        expected = "746865206b696420646f6e277420706c6179"

        v = hex ^ xorv

        self.assertEqual(v.hex, expected, "Should be " + expected)
