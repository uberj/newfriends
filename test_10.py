import unittest
import string

from CBCCipher import *
from binascii import a2b_base64


class TestChallenge10(unittest.TestCase):
	def test_decrypt_file(self):
		with open("10.txt", "r") as fd:
			e = "".join(fd.readlines())
			ciphertext = a2b_base64(e)
			cipher = CBCCipher("YELLOW SUBMARINE", "\x00" * 16)
			self.assertTrue(cipher.decrypt(ciphertext).startswith(b"I'm back and I'm ringin' the bell \nA rockin' on the mike while the fly girls yell \nIn ecstasy in the b"))

	def test_encrypt_decrypt(self):
		cipher = CBCCipher("key", "initialization vector")
		message = string.ascii_letters * 20
		e = cipher.encrypt(message.encode())
		m = cipher.decrypt(e)
		self.assertEqual(message, m.decode())
