import unittest
from Crypto.Cipher import AES
from binascii import a2b_base64, unhexlify

from thecode import *
from bitstring import BitArray as BA


class Test64(unittest.TestCase):
	def test_challenge_serialization(self):
		with open("8.txt") as fd:
			hlines = fd.readlines()
			for l in hlines:
				print(l)
				print(bytes.fromhex(l))
				print("")
