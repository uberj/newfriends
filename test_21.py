import unittest

from cipher.MersenneTwisterPRNG import MersenneTwisterPRNG


class TestChallenge21(unittest.TestCase):
	def test_transpose(self):
		r = MersenneTwisterPRNG(0)
		for i in range(1000):
			r.next()


