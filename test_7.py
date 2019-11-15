import unittest
from Crypto.Cipher import AES
from binascii import a2b_base64

from thecode import *
from bitstring import BitArray as BA


class Test64(unittest.TestCase):
	def test_challenge_serialization(self):
		with open("7.txt") as fd:
			e = a2b_base64(fd.read())
			cipher = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)
			s = cipher.decrypt(e)
			self.assertTrue(s.startswith(b"I'm back and I'm ringin' the bell"))

