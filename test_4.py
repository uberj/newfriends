import unittest

from pprint import pprint
from util import *
from bitstring import BitArray as BA


VALID_LETTERS = set(string.ascii_letters)


def valid_letter_count_percentage(candidate:BA) -> float:
	count = 0
	for c in candidate.bytes:
		if chr(c) in VALID_LETTERS:
			count += 1
	return float(count) / len(candidate.bytes)


def score_message(e:BA) -> [(int, str)]:
	scores = []
	for i in range(256):
		key = BA(hex(i)) * int((len(e) / 8))
		if len(key) < len(e):
			key = key * 2
		candidate = (e ^ key)

		scores.append((dictionary_word_count(candidate), to_str(candidate)))

	return scores


class Test64(unittest.TestCase):
	def test_example(self):
		# I guess assume these people are thinking in C
		# Single char is 1 byte (8 bit)
		scores = []
		with open("4.txt", "r") as fd:
			for line in fd.readlines():
				ba = BA("0x" + line.strip())
				scores += score_message(ba)

		print("Top 20:")
		pprint(list(reversed(sorted(scores, key=lambda x: x[0])))[:20])

		print("Best:")
		pprint(sorted(scores, key=lambda x: x[0])[-1])
