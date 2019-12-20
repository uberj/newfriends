import math

LETTER_FREQ = {
	'\n': 2.8952504879635654, 'y': 2.6675341574495772, 'o': 5.823031880286272, ',': 1.398828887443071,
	' ': 17.56668835393624, 'v': 1.1711125569290826, 'i': 6.701366297983085, 'p': 1.5289525048796355,
	'l': 4.912166558230319, 'e': 8.295380611581002, 't': 5.790500975927131, "'": 0.9433962264150944,
	's': 3.610930383864672, 'k': 1.5289525048796355, 'c': 3.4482758620689653, '!': 0.16265452179570591,
	'b': 2.47234873129473, 'a': 6.701366297983085, 'r': 2.504879635653871, 'g': 1.594014313597918,
	'h': 3.610930383864672, 'n': 4.4567338972023425, 'd': 2.5699414443721533, 'w': 1.3662979830839297,
	'm': 2.147039687703318, 'f': 0.9108653220559532, '?': 0.06506180871828238, 'u': 1.951854261548471,
	'x': 0.13012361743656475, '.': 0.16265452179570591, 'j': 0.4229017566688354, 'q': 0.06506180871828238,
	'z': 0.09759271307742355, '5': 0.03253090435914119, '0': 0.03253090435914119, '"': 0.1951854261548471,
	'1': 0.03253090435914119, '-': 0.03253090435914119}


LETTER_AS_BYTE_FREQ = dict(map(lambda el: (ord(el[0]), el[1]), LETTER_FREQ.items()))


def frequency_analysis_score(s: bytes) -> float:
	score = 0
	unique_chars = set(s)
	for c in unique_chars:
		# number of times c appears in s
		num_c_in_s = len(list(filter(lambda x: x == c, s)))

		# frequency of c in s
		p_c = (num_c_in_s / len(s)) * 100

		if c in LETTER_AS_BYTE_FREQ:
			error = math.fabs(LETTER_AS_BYTE_FREQ.get(c) - p_c * 10)
			score -= error
		else:
			score -= 300

	return score / len(unique_chars)


def transpose(xs: [bytes]) -> [bytes]:
	assert len(xs) > 1
	# Everything must be the same size
	assert len(set(list(map(len, xs)))) == 1

	transposed = []
	for i in range(len(xs[0])):
		line = []
		for x in xs:
			line.append(x[i])
		transposed.append(bytes(line))

	return transposed

