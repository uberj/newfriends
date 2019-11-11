import unittest
import base64
import sys

from pprint import pprint
from thecode import *
import math
from bitstring import BitArray as BA

KEY_SIZE = 4

def challenge_input() -> BA:
	with open("6.txt") as fd:
		e = "".join(fd.readlines())
		return str_to_ba(base64.b64decode(e).hex())

class Test64(unittest.TestCase):
	def test_best_key_size(self):
		e = challenge_input()
		best_distance = 10000
		best_size = 10000
		for guess_key_size in range(2, 31):
			b0 = e[0:guess_key_size]
			b1 = e[guess_key_size:guess_key_size*2]
			b2 = e[guess_key_size*2:guess_key_size*3]
			b3 = e[guess_key_size*3:guess_key_size*4]

			distance0 = hamming_weight(b0, b1) / float(guess_key_size)
			distance1 = hamming_weight(b2, b3) / float(guess_key_size)

			distance = (distance0 + distance1) / 2
			if distance < best_distance:
				best_distance = distance
				best_size = guess_key_size

		print("---------")
		print(best_distance) # 0.25
		print(best_size) # 4


	def test_example(self):
		a = str_to_ba("this is a test")
		b = str_to_ba("wokka wokka!!!")
		self.assertEqual(hamming_weight(a, b), 37)

