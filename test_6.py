import unittest
import base64
import sys

from pprint import pprint
from thecode import *
import math
from bitstring import BitArray as BA

#KEY_SIZE = [2, 3, 5]
KEY_SIZE = [5]


def challenge_input() -> BA:
	with open("6.txt") as fd:
		e = "".join(fd.readlines())
		decode = base64.b64decode(e)
		ba = BA("0x" + decode.hex())
		return ba


class Test64(unittest.TestCase):
	def test_best_key_size(self):
		e = challenge_input()
		distances = top_n_key_sizes(30, e)
		pprint(distances)

	def test_decrypt1(self):
		e = challenge_input()
		print(to_str(xor_cycle_encrypt(BA("eo!so".encode()), e)))

	def test_solve_for_key(self):
		e = challenge_input()
		for ks in range(3, 20):
			blocks = transpose(e, ks)
			key = ""
			for i, b in enumerate(blocks):
				map(lambda x: x[1], top_n_decrypt_key(5))
				key += best_decrypt_key(b)[1]
			print("%s: %s" % (ks, key))

	def test_bytes_to_ba(self):
		b = BA("0x0000")
		bs = [b.bytes[0], b.bytes[1]]
		self.assertEquals(BA("0x0000"), bytes_to_ba(bs))

		b = BA("0xffaa")
		bs = [b.bytes[0], b.bytes[1]]
		self.assertEquals(BA("0xffaa"), bytes_to_ba(bs))

	def test_transpose_to_str_edge_case(self):
		e = BA("0xff00aa00")
		blocks = transpose(e, 2)
		self.assertEquals(len(blocks), 2)
		self.assertEquals(BA('0xffaa'), blocks[0])
		to_str(blocks[0])
		self.assertEquals(BA('0x0000'), blocks[1])

	def test_transpose1(self):
		e = BA("0xff00aa00")
		blocks = transpose(e, 2)
		self.assertEquals(len(blocks), 2)
		self.assertEquals(BA('0xffaa'), blocks[0])
		self.assertEquals(BA('0x0000'), blocks[1])

	def test_transpose2(self):
		e = BA("0x00112233445566778899")
		blocks = transpose(e, 4)
		self.assertEqual(len(blocks), 4)
		self.assertEquals(BA('0x004488'), blocks[0])
		self.assertEquals(BA('0x115599'), blocks[1])
		self.assertEquals(BA('0x2266'), blocks[2])
		self.assertEquals(BA('0x3377'), blocks[3])

	def test_transpose3(self):
		e = BA("0x0b3637")
		blocks = transpose(e, 3)
		self.assertEqual(len(blocks), 3)
		self.assertEqual(BA('0x0b'), blocks[0])
		self.assertEqual(BA('0x36'), blocks[1])
		self.assertEqual(BA('0x37'), blocks[2])

	def test_decrypt_I_block(self):
		# Make sure that the transpose blocks allow us to detect "C" as the 2nd key char
		e = BA('0x362a632e2a3a632d632a63272a2f0a2c313a2b632b31632e2f')
		keys = top_n_decrypt_key(50, e)
		self.assertEqual("C", keys[0][1])

	def test_decrypt_sample(self):
		# Make sure we can find the right key
		a = BA("0x0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
		blocks = transpose(a, 3)
		key = ""
		for i, b in enumerate(blocks):
			key += best_decrypt_key(b)[1]
		self.assertEqual("ICE", key)

	def test_hamming_weight2(self):
		a = BA(b'this is a test')
		b = BA(b'wokka wokka!!!')
		self.assertEqual(hamming_weight(a, b), 37)

