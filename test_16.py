import unittest

from cipher.cbc import CBCCipher
from util.somecode import pad16_PKCS7, unpad16_PKCS7, rand_n_string

FIXED_KEY = rand_n_string(16).encode()
FIXED_IV = rand_n_string(16).encode()


def encrypt_data(user_data: bytes) -> bytes:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	s = b"comment1=cooking%20MCs;userdata=" \
		+ user_data.replace(b";", b"").replace(b"=", b"") \
		+ b";comment2=%20like%20a%20pound%20of%20bacon"

	return cipher.encrypt(pad16_PKCS7(s))


def decrypt(blob: bytes) -> bytes:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	decrypt = cipher.decrypt(blob)
	unpaded = unpad16_PKCS7(decrypt)
	return unpaded


def check_admin(blob: bytes) -> bool:
	b = decrypt(blob)
	return b";admin=true;" in b


class TestChallenge16(unittest.TestCase):
	def test_plain(self):
		cipher_text = encrypt_data(b"XXXXXX")
		admin_check = check_admin(cipher_text)
		self.assertFalse(admin_check)

	def test_attack(self):
		"""
		Here are the blocks!

		comment1=cooking (0:15)
		%20MCs;userdata= (16:31)
		(User here)
		;comment2=%20lik
		e%20a%20pound%20
		of%20bacon

		I want something like:

		comment1=cooking (0:15)
		%20MCs;userdata= (16:31)
		YYYYYYYYYYYYYYYY (32:47)
		;admin=true;XXXX (48:64)
		;comment2=%20lik (80:)

		ord(":") -> 58
		bin(58) -> 0b111010
		--- change 1 bit ---
		0b111010 ^ 0b000001 -> 0b111011
		0b111011 -> 59
		chr(59) -> ";"

		Simplified and expanded to the other character:
		chr(ord(':') ^ 0b000001) -> ';'
		chr(ord('=') ^ 0b000001) -> '<'

		Following rules I can get:

		0123456789012345
		YYYYYYYYYYYYYYYY (32:47)
		:admin>true:XXXX (48:64)

		I encrypt...
		I take my encrypted "YY.." block...
		I change the (32)th, (32 + 6)th, and (32 + 11)th  byte to "0b000001"

		I check admin on that.
		Let us see if that works!
		(Will try later)

		This didn't work (I didn't know why at first).
		My trick was to brute force the bit flips I needed.

		What I was really missing was that I actually only needed to change one bit.
		In fact, I only *want* to change one bit.
		When I was setting the flip bits to \x01 it was flipping more bits than I wanted
		To only flip one bit:

		cur_attack_block[pos] ^ 1

		That was the trick!


		:return:
		"""
		crafted_block = b'YYYYYYYYYYYYYYYY:admin<true:XXXX'
		data = encrypt_data(crafted_block)
		bit_flip_targets = [(32, ';'), (32 + 6, '='), (32 + 11, ';')]
		cur_attack_block = data
		for pos, target in bit_flip_targets:
			i = cur_attack_block[pos] ^ 1
			cur_attack_block = cur_attack_block[0:pos] + bytes([i]) + cur_attack_block[pos + 1:]
		self.assertIsNotNone(cur_attack_block)
		self.assertTrue(check_admin(cur_attack_block))

