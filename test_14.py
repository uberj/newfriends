import unittest
import os
from Crypto.Cipher import AES

from ecb_util import ordered_block_counts
from oracle import oracle_guess_cipher_type, BBoxType, oracle_guess_ecb_block_sizes
from set1 import rand_n_string, pad16_PKCS7
from binascii import a2b_base64
from sample_text import text as SAMPLE_TEXT
from random import randint

CHALLANGE_CIPHER_TEXT = a2b_base64("""Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")
FIXED_KEY = rand_n_string(16)
RANDOM_PREFIX = rand_n_string(randint(5, 100)).encode()


def oracle_encrypt(known_text: bytes) -> bytes:
	return encrypt_(RANDOM_PREFIX, known_text, CHALLANGE_CIPHER_TEXT)


def encrypt_(random_prefix: bytes, known_text: bytes, unknown_text: bytes) -> bytes:
	cipher = AES.new(FIXED_KEY, AES.MODE_ECB)
	box_content = cipher.encrypt(pad16_PKCS7(random_prefix + known_text + unknown_text))
	return box_content


def detect_prefix_details() -> (int, int):
	"""
	Assuming the 16 byte block size.
	We need to detect the length of the random prefix. Here's how:
		* Loop over n=0 -> n=15
		* Pass in ("X" * n + A * 32)
			* If we see two duplicate blocks in the output, we know the prefix is n (mod 16)
		* Use existing code from 12 but prepend "X" * n to the attack string
	"""
	expected_dupe_count = 17 # We should only see this number of dupes if the blocks line up
	block_size = 16
	for n in range(block_size):
		tester = n * b"X" + b"A" * (block_size * expected_dupe_count)
		cipher_text = oracle_encrypt(tester)
		counts = ordered_block_counts(cipher_text, block_size)
		test_count = counts[0]
		if test_count[1] == expected_dupe_count:
			subs = test_count[0]
			return cipher_text.index(subs) - n, n

	raise Exception("couldn't find prefix details")


def decrypt_unknown(block_size: int, prefix_start: int, prefix_pad_len: int) -> str:
	"""
	Attack the oracle
	:param block_size: How large is the cipherblock (going to be 16 bytes for this exercise. we could detect it though)
	:param prefix_start: The index of the byte at which the random prefix ends
	:param prefix_pad_len: How many bytes to pad to get the random prefix to line up on block boundaries
	:return: Decrypted plain text
	"""
	plain_text = ""
	# Bit of a cheat here, but you could detect it if you really wanted to just using the oracle
	num_bytes_to_guess = (len(SAMPLE_TEXT) % block_size) * block_size
	prefix_pad = b'X' * prefix_pad_len
	total_prefix_len = prefix_start + prefix_pad_len
	for byte_target in reversed(range(0, num_bytes_to_guess)):
		oracle_block = b'A' * byte_target
		e = oracle_encrypt(prefix_pad + oracle_block)
		possibles = {}
		for i in range(255):
			test_block = oracle_block + plain_text.encode() + chr(i).encode()
			test_output_block = oracle_encrypt(prefix_pad + test_block)
			oracle_input_size = len(test_block)
			size_ = test_output_block[total_prefix_len:total_prefix_len + oracle_input_size]
			possibles[size_] = test_block

		target_block = e[total_prefix_len:total_prefix_len + len(oracle_block) + len(plain_text.encode()) + 1]
		ith_byte = possibles[target_block][-1]
		plain_text += chr(ith_byte)

	return plain_text


class TestChallenge14(unittest.TestCase):
	def test_detect_prefix_details(self):
		prefix_start, prefix_pad_len = detect_prefix_details()
		self.assertEqual(len(RANDOM_PREFIX), prefix_start)
		self.assertEqual(16 - (len(RANDOM_PREFIX) % 16), prefix_pad_len)
		self.assertEqual(0, (prefix_pad_len + prefix_start) % 16)

	def test_plan(self):
		prefix_start, prefix_pad_len = detect_prefix_details()
		plain_text = decrypt_unknown(16, prefix_start, prefix_pad_len)
		print(plain_text)
		self.assertTrue(plain_text.startswith("Rollin' in my 5.0"))

