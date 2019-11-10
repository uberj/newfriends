import string
import math

from bitstring import BitArray as BA


LETTER_FREQ = {
	"a": 8.167,
	"b": 1.492,
	"c": 2.782,
	"d": 4.253,
	"e": 12.702,
	"f": 2.228,
	"g": 2.015,
	"h": 6.094,
	"i": 6.966,
	"j": 0.153,
	"k": 0.772,
	"l": 4.025,
	"m": 2.406,
	"n": 6.749,
	"o": 7.507,
	"p": 1.929,
	"q": 0.095,
	"r": 5.987,
	"s": 6.327,
	"t": 9.056,
	"u": 2.758,
	"v": 0.978,
	"w": 2.360,
	"x": 0.150,
	"y": 1.974
}

ALL_CHARS_BASE64 = list(string.ascii_uppercase) \
                   + list(string.ascii_lowercase) \
                   + list(string.digits) \
                   + ["+", "/"]


def ints_to_hex(ints:[int]) -> str:
	s = ""
	for i in ints:
		s += hex(i)[2:].rjust(4, "0")
	return s

"""
Converts hex "abcde" -> 32-bit-numbers [32, 23, 34]
"""
def hex_to_ints(hex_s:str) -> [int]:
	if len(hex_s) % 2 == 1:
		hex_s = "0" + hex_s
	cur = 0
	empty_cur = True
	ns = []
	for i in range(0, len(hex_s) - 1, 2):
		b0 = int(hex_s[i], 16)
		b1 = int(hex_s[i + 1], 16)
		empty_cur = False
		if i != 0 and i % 3 == 0:
			ns.append(cur)
			cur = 0
			empty_cur = True
		cur = (cur << 8) + (b0 << 4) + b1

	if not empty_cur:
		ns.append(cur)

	return ns


def int_to_sextet(tb:int) -> [int]:
	f3 = tb & 63
	tb = tb >> 6
	f2 = tb & 63
	tb = tb >> 6
	f1 = tb & 63
	tb = tb >> 6
	f0 = tb & 63
	return [f0, f1, f2, f3]


def hex_to_base64(hex_s:str) -> str:
	s = ""
	ints = hex_to_ints(hex_s)
	for i in ints:
		sextets = int_to_sextet(i)
		for sext in sextets:
			s += ALL_CHARS_BASE64[sext]

	return s


def zip_bytes(buff0, buff1, default=0) -> [(int, int)]:
	for i in range(max(len(buff0), len(buff1))):
		a = default
		b = default
		if i < len(buff0):
			a = buff0[i]
		if i < len(buff1):
			b = buff1[i]
		yield (a, b)


"""
xor two lists streams of ints
"""
def xor(buff0:[int], buff1:[int]) -> [int]:
	r = []
	for i0, i1 in zip_bytes(buff0, buff1):
		r.append(i0 ^ i1)
	return r


def word_dictionary():
	with open("/usr/share/dict/words", "r") as fd:
		return set([word.strip() for word in fd.readlines()])


WORD_DICTIONARY = word_dictionary()


def dictionary_word_count(candidate:BA):
	s = to_str(candidate)
	count = 0
	split = s.split(" ")
	for word in split:
		if word in WORD_DICTIONARY:
			count += 1
	return float(count) / len(split)


def to_str(candidate: BA) -> str:
	return "".join([chr(b) for b in candidate.bytes])


def str_to_ba(i:str) -> BA:
	h = "0x"
	for c in i:
		h += hex(ord(c))
	return BA(h)


VALID_LETTERS = set(string.ascii_letters)


def valid_letter_count_percentage(candidate:BA) -> float:
	count = 0
	for c in candidate.bytes:
		if chr(c) in VALID_LETTERS:
			count += 1
	return float(count) / len(candidate.bytes)


def realistic_letter_distribution(candidate:BA) -> float:
	s = to_str(candidate).lower()

	score = 0
	uniq_chars = set(s)
	for c in uniq_chars:
		num_c_in_s = len(list(filter(lambda x: x == c, s)))
		p_c = (num_c_in_s / len(s)) * 100
		if c in LETTER_FREQ:
			t = math.fabs(LETTER_FREQ.get(c) - p_c)
			score += 1/t

	return score / len(uniq_chars)
