c_to_a_64_ = [
	"A",
	"B",
	"C",
	"D",
	"E",
	"F",
	"G",
	"H",
	"I",
	"J",
	"K",
	"L",
	"M",
	"N",
	"O",
	"P",
	"Q",
	"R",
	"S",
	"T",
	"U",
	"V",
	"W",
	"X",
	"Y",
	"Z",
	"a",
	"b",
	"c",
	"d",
	"e",
	"f",
	"g",
	"h",
	"i",
	"j",
	"k",
	"l",
	"m",
	"n",
	"o",
	"p",
	"q",
	"r",
	"s",
	"t",
	"u",
	"v",
	"w",
	"x",
	"y",
	"z",
	"0",
	"1",
	"2",
	"3",
	"4",
	"5",
	"6",
	"7",
	"8",
	"9",
	"+",
	"/",
]

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
			s += c_to_a_64_[sext]

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

