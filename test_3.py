import unittest
import math

from thecode import *
from bitstring import BitArray as BA


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


def candidate_score(candidate):
	counts = {}
	for b in candidate.bytes:
		s = chr(b)
		counts.setdefault(s, 0)
		counts[s] += 1

	distro = {}
	for l, c in counts.items():
		distro[l] = (float(c) / len(candidate.bytes)) * 100

	total_error = 0
	for l, freq in distro.items():
		if l not in LETTER_FREQ:
			total_error += 1
			continue
		total_error += math.fabs(freq - LETTER_FREQ.get(l))

	return total_error / len(distro.items())


def to_str(candidate: BA) -> str:
	return "".join([chr(b) for b in candidate.bytes])


def find_best_message(e:BA) -> str:
	scores = []
	for c in map(chr, range(256)):
		i = ord(c)
		key = BA(hex(i) * len(e.bytes))
		if len(key) < len(e):
			key = key * 2
		if i == 88:
			print("Best key:" + str(key))
		candidate = (e ^ key)

		scores.append((dictionary_word_count(candidate), c, to_str(candidate)))

	best = sorted(scores, key=lambda x: x[0])[-1]
	print(ord(best[1]))
	return best[2]


class Test64(unittest.TestCase):
	def test_decrypt(self):
		# I guess assume these people are thinking in C
		# Single char is 1 byte (8 bit)
		e = BA("0x1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
		self.assertEqual("Cooking MC's like a pound of bacon", find_best_message(e))

		d0 = BA(hex(ord('k')) * len(e.bytes))
		print((e ^ d0).hex)

		key = find_best_key(e)
		d = BA(hex(ord(key)) * len(e.bytes))
		self.assertEqual("Cooking MC's like a pound of bacon", to_str(e ^ d))
