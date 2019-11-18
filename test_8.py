import unittest
import random
from Crypto.Cipher import AES
from binascii import a2b_base64, unhexlify, hexlify
import os

from thecode import *
from bitstring import BitArray as BA
ENTRY_SIZE = 160


def encrypted_needle():
	cipher = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)
	encrypt = cipher.encrypt(pad_PKCS7("""Yo, VIP, let's kick it!

Ice Ice Baby, Ice Ice Baby

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaon
Something grabs a hold of"""))
	return hexlify(encrypt)


def hay():
	return hexlify(os.urandom(ENTRY_SIZE))


def build_haystack():
	haystack = []
	for i in range(400):
		haystack.append(hexlify(hay()))
	return haystack


def place(needle: str, haystack: [str]):
	haystack[random.randint(0, len(haystack))] = needle


def find_needle(haystack: [str]) -> str:
	counts = map(lambda s: (s, count_identical_blocks(s)), haystack)
	return pick_highest_dupe_count(counts)


def count_identical_blocks(s):
	counts = {}
	for i in range(0, len(s), 16):
		c = "".join(map(chr, s[i:i+16]))
		counts.setdefault(c, 0)
		counts[c] += 1
	return counts


def pick_highest_dupe_count(counts):
	scounts = list(reversed(sorted(counts, key=lambda c: max(c[1].values()))))
	return scounts[0]


class Test64(unittest.TestCase):
	def test_pick_highest_dupe_count(self):
		h = ("high", {'9c0ffed98dacd070': 1, '425bebdb68de6f56': 1, 'a1da151e74743ac2': 1, 'f95a2a504ad1f806': 1, '845373ec2c145f20': 1, 'ca1a9f2c3ab5938f': 1, 'd0bfa219c0f0830b': 1, 'f599b825835f1166': 1, 'da030c17f299c08f': 3, '5f63527b29ed520f': 3, 'fdaff1e2b1fa1cae': 1, 'ffa2cd4cece3dc02': 1, 'accaa77fb250084f': 1, 'bda0c4d973bf68b5': 1, 'c00a9f39ebd60fd4': 1, 'f6347194fc3155c5': 1})
		l = ("low", {'680446590e4b0409': 1, '254cd301ff6445ac': 1, '0600c2f448619076': 1, 'd77bd5afdb4faca9': 1, 'e066c90e0b1d2ec8': 1, 'b73c87aefee39c9a': 1, '911ad9783b4c5af0': 1, '188273d94733c630': 1, 'c5607a6a6049a3a8': 1, '6f0c4320ed3e4451': 1, '7153934a620d860e': 1, '3aca5232da437966': 1, '3757580ee6c3d565': 1, '8d24da8589f7f501': 1, 'f9dccac2653d8f18': 1, '5cb9997432d2bbcc': 1, '616a82c768935f6c': 1, '5e81ad56e4376fe0': 1, '55a984b93dec9bae': 1, '4c59aebb9c202303': 1})
		self.assertEqual("high", pick_highest_dupe_count([h, l])[0])


	def test_generate_encrypted_line_and_find(self):
		needle = encrypted_needle()
		haystack = build_haystack()
		place(needle, haystack)
		s = find_needle(haystack)
		self.assertEqual(needle, s[0])

	@unittest.SkipTest
	def test_challenge_find_encrypted_line(self):
		with open("8.txt") as fd:
			hlines = map(lambda s: s.encode(), fd.readlines())
			pprint(find_needle(hlines)[0])
