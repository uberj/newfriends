import unittest

from crypto.ctr import CTRCipher
from util.somecode import rand_n_string
import random

FIXED_KEY = rand_n_string(16).encode()
FIXED_IV = random.randint(0, 2**32)


def encrypt_data(user_data: bytes) -> bytes:
	cipher = CTRCipher(FIXED_KEY, FIXED_IV)
	s = b"comment1=cooking%20MCs;userdata=" \
	    + user_data.replace(b";", b"").replace(b"=", b"") \
	    + b";comment2=%20like%20a%20pound%20of%20bacon"

	return cipher.encrypt(s)


def decrypt(blob: bytes) -> bytes:
	cipher = CTRCipher(FIXED_KEY, FIXED_IV)
	return cipher.decrypt(blob)


def check_admin(blob: bytes) -> bool:
	b = decrypt(blob)
	return b";admin=true;" in b


class TestChallenge26(unittest.TestCase):
	def test_plain(self):
		cipher_text = encrypt_data(b"XXXXXX")
		admin_check = check_admin(cipher_text)
		self.assertFalse(admin_check)

	def test_attack(self):
		"""
		I want something like:

		comment1=cooking (0:15)
		%20MCs;userdata= (16:31)
		;admin=true;XXXX (32:47)
		;comment2=%20lik (80:)
		"""
		crafted_block = b':admin<true:XXXX'
		data = encrypt_data(crafted_block)
		bit_flip_targets = [(32, ';'), (32 + 6, '='), (32 + 11, ';')]
		cur_attack_block = data
		for pos, target in bit_flip_targets:
			i = cur_attack_block[pos] ^ 1
			cur_attack_block = cur_attack_block[0:pos] + bytes([i]) + cur_attack_block[pos + 1:]
		self.assertIsNotNone(cur_attack_block)
		self.assertTrue(check_admin(cur_attack_block))
