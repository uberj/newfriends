import unittest

from util.somecode import rand_n_string

FIXED_KEY = rand_n_string(16).encode()

class TestChallenge25(unittest.TestCase):
	def test_(self):
		pass
