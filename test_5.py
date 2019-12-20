import unittest
import sys

from util.somecode import *
import math
from bitstring import BitArray as BA


def xor_cycle_encrypt(key:BA, m:BA) -> BA:
	e = key * math.ceil(float(len(m))/len(key))
	e = e[:len(m)]

	assert len(e) == len(m)

	return e ^ m


def xor_encrypt(key_text, ms) -> str:
	key_ = BA(key_text.encode())
	encrypt = xor_cycle_encrypt(key_, BA(ms.encode()))
	return encrypt.hex


def xor_encrypt_ba(key_text: bytes, ms: bytes) -> BA:
	key_ = BA(key_text)
	encrypt = xor_cycle_encrypt(key_, BA(ms))
	return encrypt


class TestChallenge5(unittest.TestCase):
	def test_example(self):
		x = b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
		e = xor_encrypt_ba(b'ICE', x)
		a_ = BA("0x0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
		self.assertEqual(e, a_)

	@unittest.SkipTest
	def test_end_to_end(self):
		e = xor_encrypt_ba(b'ICE', SAMPLE_TEXT.encode())
		print(to_str(e))
		t = top_n_key_sizes(20, e)
		pprint(t)
		blocks = transpose(e, 3)
		key = ""
		for i, b in enumerate(blocks):
			key += best_decrypt_key(b)[1]
		print(key)
		m = to_str(xor_cycle_encrypt(BA(key.encode()), e))
		print(m)


if __name__ == "__main__":
	key = sys.argv[1]
	print(xor_encrypt(key, sys.stdin.read()))
