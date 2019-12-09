import unittest
from random import choice

from CBCCipher import CBCCipher
from somecode import pad16_PKCS7, unpad16_PKCS7, rand_n_string, PaddingException

FIXED_KEY = rand_n_string(16).encode()
FIXED_IV = rand_n_string(16).encode()

PSTRINGS = [
	b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
	b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
	b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
	b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
	b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
	b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
	b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
	b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
	b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
	b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]


def cipher_text_provider() -> (bytes, bytes):
	c0 = choice(PSTRINGS)
	p = pad16_PKCS7(c0)
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	return FIXED_IV, cipher.encrypt(p)


def padding_oracle(cipher_text) -> bool:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	decrypt = cipher.decrypt(cipher_text)
	try:
		unpad16_PKCS7(decrypt)
	except PaddingException:
		return False
	return True


class TestChallenge17(unittest.TestCase):
	def test_select_string(self):
		iv, cipher_text = cipher_text_provider()
		self.assertIsNotNone(iv)
		self.assertIsNotNone(cipher_text)

	def test_consumer(self):
		iv, cipher_text = cipher_text_provider()

		pad_test0 = padding_oracle(cipher_text)
		self.assertTrue(pad_test0)

		pad_test1 = padding_oracle(cipher_text[2:] + b"\xff" + b"\xff")
		self.assertFalse(pad_test1)
