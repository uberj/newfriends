import unittest
import os
from Crypto.Cipher import AES

from oracle import oracle_guess_cipher_type, BBoxType, oracle_guess_ecb_block_sizes
from set1 import rand_n_string, pad_PKCS7
from binascii import a2b_base64
from sample_text import text as SAMPLE_TEXT

CHALLANGE_CIPHER_TEXT = a2b_base64("""Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")
FIXED_KEY = rand_n_string(16)


def encrypt(known_text: bytes) -> bytes:
	return encrypt_(known_text, CHALLANGE_CIPHER_TEXT)


def encrypt_(known_text: bytes, unknown_text: bytes) -> bytes:
	cipher = AES.new(FIXED_KEY, AES.MODE_ECB)
	box_content = cipher.encrypt(pad_PKCS7(known_text + unknown_text))
	return box_content


def decrypt_unknown(block_size: int) -> str:
	plain_text = b''
	for byte_target in range(block_size - 1, 100):  # not sure how to end it
		oracle_block = b'A' * byte_target
		e = encrypt(oracle_block)
		possibles = {}
		for i in range(255):
			test_block = oracle_block + chr(i).encode()
			test_output_block = encrypt(test_block)
			possibles[test_block] = test_output_block[0:block_size]

		target_block = e[0:block_size]
		ith_byte = possibles[target_block][-1]
		plain_text += ith_byte
		break

	return plain_text.decode()


class TestChallenge12(unittest.TestCase):
	def test_plan(self):
		long_duplicated_plaintext = SAMPLE_TEXT
		long_duplicated_ciphertext = encrypt(long_duplicated_plaintext.encode())
		guess = oracle_guess_cipher_type(long_duplicated_ciphertext)
		self.assertEqual(guess, BBoxType.ECB)

		sizes = oracle_guess_ecb_block_sizes(long_duplicated_ciphertext)
		best_block_size = sizes[0]
		self.assertEqual(16, best_block_size)  # We know in this example, so just make sure our code knows
		plain_text = decrypt_unknown(best_block_size)

