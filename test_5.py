import unittest
import sys

from pprint import pprint
from util import *
import math
from bitstring import BitArray as BA

def str_to_ba(i:str) -> BA:
	h = "0x"
	for c in i:
		h += hex(ord(c))
	return BA(h)

def xor_cycle_encrypt(key:BA, m:BA) -> BA:
	e = key * math.ceil(float(len(m))/len(key))
	e = e[:len(m)]

	assert len(e) == len(m)

	return e ^ m


def ba_to_hex(encrypt:BA) -> str:
	return encrypt.hex


def xor_encrypt(key_text, ms) -> str:
	key = str_to_ba(key_text)
	es = []
	encrypt = xor_cycle_encrypt(key, str_to_ba(ms))
	es.append(ba_to_hex(encrypt))
	return "\n".join(es)


class Test64(unittest.TestCase):
	def test_example(self):
		x = "Burning 'em, if you ain't quick and nimble\r\nI go crazy when I hear a cymbal"
		e = xor_encrypt("ICE", x)
		# a_ = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
		a_ =   "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20930a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
		self.assertEqual(e, a_)

if __name__ == "__main__":
	key = sys.argv[1]
	print(xor_encrypt(key, sys.stdin.read()))
