import unittest

from somecode import *
from bitstring import BitArray as BA


class TestChallenge4(unittest.TestCase):
	def test_letter_distribution(self):
		ba1 = BA(b'He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and fishery rihgts at once. He was the more ready to do this becuase the rights had becom much less valuable, and he had indeed the vaguest idea where the wood and river in quedtion were.')
		s1 = realistic_letter_distribution(ba1)

		ba2 = BA(b'kjafjkf adfsjkafdsj 345oislnasdlkj qlktj oqeijg 0340hqi0jwqicdwjiwkpqwop lmknxlmc,zmcj adfi  iu qwpjaljkdfjdslk f.jk.mcvnvcn vndpijpifuw9- kls adlksajm.slksapij dfp- qw jkasjkad djkadsnkvlsadkjaw 9 e2j jadjlkadladfs jklajk ej ;j awefjlkasadjw pjowe ew ipjewji ewj iwejfal kas advpceq qe 9')
		s2 = realistic_letter_distribution(ba2)

		self.assertTrue(s1 > s2)

	def test_letter_distribution1(self):
		ba1 = BA(b'Cooking MC\'s like a pound of bacon')
		s1 = realistic_letter_distribution(ba1)

		ba2 = BA("0x705c5c585a5d54137e701440135f5a5856135213435c465d57135c55135152505c5d")
		s2 = realistic_letter_distribution(ba2)

		self.assertTrue(s1 > s2)

	def test_letter_distribution2(self):
		good = BA("0x7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f")
		s1 = realistic_letter_distribution(good)

		fake = BA("0x1c3df1135321a8e9241a5607f8305d571aa546001e3254555a11511924")
		s2 = realistic_letter_distribution(fake)

		self.assertTrue(s1 > s2)

	def test_letter_distribution3(self):
		good = 'Now that the party is jumping\n'
		s1 = realistic_letter_distribution_(good)

		fake = 'hI\x85g\'UÜ\x9dPn"s\x8cD)#nÑ2tjF !.e%mP'
		s2 = realistic_letter_distribution_(fake)

		self.assertTrue(s1 > s2)

	def test_letter_distribution4(self):
		fake = 'th!lhx!o!h!ehmHnsxi!is!lm'
		s2 = realistic_letter_distribution_(fake)

		good = 'ui miy n i dilIoryh hr ml'
		s1 = realistic_letter_distribution_(good)

		self.assertTrue(s1 > s2)

	@unittest.SkipTest
	def test_example(self):
		# I guess assume these people are thinking in C
		# Single char is 1 byte (8 bit)
		scores = []
		blocks = []
		with open("4.txt", "r") as fd:
			for line in fd.readlines():
				ba = BA("0x" + line.strip())
				blocks.append(ba)

		for block in blocks:
			scores.append(best_decrypt_key(block))

		best = list(reversed(sorted(scores, key=lambda x: x[0])))
		self.assertEqual(best[0][2], "Now that the party is jumping\n")
