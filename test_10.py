import unittest
import string

from cipher.cbc import *
from binascii import a2b_base64
from binascii import a2b_hex


class TestChallenge10(unittest.TestCase):
	def test_ietf_vectors_one_blocks(self):
		# https://tools.ietf.org/html/rfc3602#section-4
		key = a2b_hex("06a9214036b8a15b512e03d534120006")
		iv = a2b_hex("3dafba429d9eb430b422da802c9fac41")
		plaintext = b"Single block msg"
		cipher_text = a2b_hex("e353779c1079aeb82708942dbe77181a")
		cipher = CBCCipher(key, iv)
		encrypt = cipher.encrypt(plaintext)
		self.assertEqual(cipher_text, encrypt)
		decrypt = cipher.decrypt(encrypt)
		self.assertEqual(plaintext, decrypt)

	def test_ietf_vectors_two_blocks(self):
		# https://tools.ietf.org/html/rfc3602#section-4
		key = a2b_hex("c286696d887c9aa0611bbb3e2025a45a")
		iv = a2b_hex("562e17996d093d28ddb3ba695a2e6f58")
		plaintext = a2b_hex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
		cipher_text = a2b_hex("d296cd94c2cccf8a3a863028b5e1dc0a7586602d253cfff91b8266bea6d61ab1")
		cipher = CBCCipher(key, iv)
		encrypt = cipher.encrypt(plaintext)
		self.assertEqual(cipher_text, encrypt)
		decrypt = cipher.decrypt(encrypt)
		self.assertEqual(plaintext, decrypt)

	def test_decrypt_file(self):
		with open("challenge_inputs/10.txt", "r") as fd:
			e = "".join(fd.readlines())
			ciphertext = a2b_base64(e)
			cipher = CBCCipher("YELLOW SUBMARINE".encode(), b"\x00" * 16)
			self.assertTrue(cipher.decrypt(ciphertext).startswith(b"I'm back and I'm ringin' the bell \nA rockin' on the mike while the fly girls yell \nIn ecstasy in the b"))

	def test_encrypt_decrypt(self):
		cipher = CBCCipher("THE TIME IS NOW!".encode(), "initialization vector".encode())
		message = string.ascii_letters * 20
		e = cipher.encrypt(message.encode())
		m = cipher.decrypt(e)
		self.assertEqual(message, m.decode())
