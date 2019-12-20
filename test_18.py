import unittest
from cipher.ctr import CTRCipher
from binascii import a2b_base64


class TestChallenge18(unittest.TestCase):
	def test_decrypt(self):
		cipher_text = a2b_base64(b'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
		ctr = CTRCipher(b'YELLOW SUBMARINE', 0)
		decrypt = ctr.decrypt(cipher_text)
		self.assertEquals(b"Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby ", decrypt)

	def test_encrypt_decrypt(self):
		ctr = CTRCipher(b'YELLOW SUBMARINE', 2874)
		i = b'YELLOW SUBMARINE YEAH!'
		cipher_text = ctr.encrypt(i)
		decrypt = ctr.decrypt(cipher_text)
		self.assertEquals(i, decrypt)
