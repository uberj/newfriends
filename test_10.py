import unittest
import string

from set2 import *
from binascii import a2b_base64


class TestChallenge10(unittest.TestCase):
	@unittest.SkipTest
	def test_decrypt_file(self):
		with open("10.txt", "r") as fd:
			e = "".join(fd.readlines())
			ciphertext = a2b_base64(e)
			cipher = CBCCipher("YELLOW SUBMARINE", "\x30" * 16)
			print(cipher.decrypt(ciphertext))

	def test_encrypt_decrypt(self):
		cipher = CBCCipher("key", "initialization vector")
		message = string.ascii_letters * 20
		e = cipher.encrypt(message)
		m = cipher.decrypt(e)
		self.assertEqual(message, m.decode())
