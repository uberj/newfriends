def triple_convert(to_convert):
	pass


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


"""
Converts hex "abcde" -> 32-bit-numbers [32, 23, 34]
"""
def hex_to_triple_bytes(hexS):
	cur = 0
	empty_cur = True
	ns = []
	for i in range(0, len(hexS) - 1, 2):
		b0 = int(hexS[i], 16)
		b1 = int(hexS[i + 1], 16)
		empty_cur = False
		if i != 0 and i % 3 == 0:
			ns.append(cur)
			cur = 0
			empty_cur = True
		cur = (cur << 8) + (b0 << 4) + b1

	if not empty_cur:
		ns.append(cur)

	return ns


def tb_to_sextet(tb) -> [int]:
	f3 = tb & 63
	tb = tb >> 6
	f2 = tb & 63
	tb = tb >> 6
	f1 = tb & 63
	tb = tb >> 6
	f0 = tb & 63
	return [f0, f1, f2, f3]


def hex_to_base64(hexS):
	s = ""
	triple_bytes = hex_to_triple_bytes(hexS)
	for tb in triple_bytes:
		sextets = tb_to_sextet(tb)
		for sext in sextets:
			s += c_to_a_64_[sext]

	return s

