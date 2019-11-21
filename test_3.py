import unittest
import math

from set1 import *
from bitstring import BitArray as BA


def find_best_message(e:BA) -> str:
	scores = []
	for c in map(chr, range(256)):
		i = ord(c)
		key = BA(hex(i) * len(e.bytes))
		if len(key) < len(e):
			key = key * 2
		candidate = (e ^ key)

		scores.append((dictionary_word_count(candidate), c, to_str(candidate)))

	best = sorted(scores, key=lambda x: x[0])[-1]
	return best[2]


class TestChallenge3(unittest.TestCase):
	def test_decrypt(self):
		# I guess assume these people are thinking in C
		# Single char is 1 byte (8 bit)
		e = BA("0x1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
		self.assertEqual("Cooking MC's like a pound of bacon", find_best_message(e))

		key = find_best_key(e)
		d = BA(hex(ord(key)) * len(e.bytes))
		self.assertEqual("Cooking MC's like a pound of bacon", to_str(e ^ d))
