import unittest
from pprint import pprint

from MersenneTwisterPRNG import MersenneTwisterPRNG
import time

def invert_temper(y):
	pass

class TestChallenge23(unittest.TestCase):
	def test_invert_temper(self):
		prng = MersenneTwisterPRNG(0)
		i = 2 ** 32 - 1
		temper = prng.temper(i)
		untemper = prng.invert_temper(temper)
		self.assertEquals(bin(untemper), bin(i))

	def test_masks(self):
		zp = lambda x: (bin(x)[2:]).rjust(32, "0")
		pprint(list(map(zp, MersenneTwisterPRNG.top_bom_masks(7))))
