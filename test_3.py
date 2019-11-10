import unittest

from util import *


def duplicate_to_int(d):
	t = (d << 8) + d
	t = (t << 8) + d
	t = (t << 8) + d
	t = (t << 8) + d
	return t


def int_to_chars(i):
	return [
		chr((i & int("0fff", 16) >> 24)),
		chr((i & int("f0ff", 16) >> 16)),
		chr((i & int("ff0f", 16) >> 8)),
		chr((i & int("fff0", 16)))
	]


class Test64(unittest.TestCase):
	def test_simple_zeros(self):
		# I guess assume these people are thinking in C
		# Single char is 1 byte (8 bit)
		e = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
		bs = hex_to_ints(e)
		for d in range(0, 2 ** 8):  # Just a guess that its one of these
			bs = hex_to_ints(e)
			buffD = [duplicate_to_int(d)] * len(bs)
			de = xor(buffD, bs)
			chars = []
			for i in de:
				to_chars = int_to_chars(i)
				chars += to_chars
			try:
				print("".join(chars))
			except:
				continue
