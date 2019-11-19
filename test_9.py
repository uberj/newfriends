import unittest
import string

from set2 import *


class Test64(unittest.TestCase):
	def test_encrypt_decrypt(self):
		cipher = CBCCipher("key", "initialization vector")
		message = string.ascii_letters * 20
		e = cipher.encrypt(message)
		m = cipher.decrypt(e)
		self.assertEqual(message, m)
