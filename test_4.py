import unittest
import math

from pprint import pprint
from thecode import *
from bitstring import BitArray as BA



def score_message(e:BA) -> [(int, str)]:
	scores = []
	for i in range(256):
		key = BA(hex(i)) * int((len(e) / 8))
		if len(key) < len(e):
			key = key * 2
		candidate = (e ^ key)

		scores.append((realistic_letter_distribution(candidate), to_str(candidate)))

	return scores


class Test64(unittest.TestCase):
	def test_letter_distribution(self):
		ba1 = str_to_ba("He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and fishery rihgts at once. He was the more ready to do this becuase the rights had becom much less valuable, and he had indeed the vaguest idea where the wood and river in quedtion were.")
		s1 = realistic_letter_distribution(ba1)

		ba2 = str_to_ba("kjafjkf adfsjkafdsj 345oislnasdlkj qlktj oqeijg 0340hqi0jwqicdwjiwkpqwop lmknxlmc,zmcj adfi  iu qwpjaljkdfjdslk f.jk.mcvnvcn vndpijpifuw9- kls adlksajm.slksapij dfp- qw jkasjkad djkadsnkvlsadkjaw 9 e2j jadjlkadladfs jklajk ej ;j awefjlkasadjw pjowe ew ipjewji ewj iwejfal kas advpceq qe 9")
		s2 = realistic_letter_distribution(ba2)

		self.assertTrue(s1 > s2)

	def test_example(self):
		# I guess assume these people are thinking in C
		# Single char is 1 byte (8 bit)
		scores = []
		with open("4.txt", "r") as fd:
			for line in fd.readlines():
				ba = BA("0x" + line.strip())
				scores += score_message(ba)

		# print("Top 20:")
		# pprint(list(reversed(sorted(scores, key=lambda x: x[0])))[:20])
		#
		# print("Best:")
		# pprint(sorted(scores, key=lambda x: x[0])[-1])
		best = sorted(scores, key=lambda x: x[0])[-1]
		self.assertEqual(best[1], "Now that the party is jumping\n")
