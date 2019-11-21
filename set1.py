import string
import math
import random

from pprint import pprint
from bitstring import BitArray as BA

SAMPLE_TEXT = """
Yo, VIP, let's kick it!

Ice Ice Baby, Ice Ice Baby

All right stop, Collaborate and listen
Ice is back with my brand new invention
Something grabs a hold of me tightly
Flow like a harpoon daily and nightly
Will it ever stop? Yo, I don't know
Turn off the lights and I'll glow
To the extreme I rock a mic like a vandal
Light up a stage and wax a chump like a candle.

Dance, go rush the speaker that booms
I'm killing your brain like a poisonous mushroom
Deadly, when I play a dope melody
Anything less than the best is a felony
Love it or leave it, you better gain way
You better hit bull's eye, the kid don't play

If there was a problem, yo, I'll solve it
Check out the hook while my DJ revolves it

Ice Ice Baby Vanilla, Ice Ice Baby Vanilla
Ice Ice Baby Vanilla, Ice Ice Baby Vanilla

Now that the party is jumping
With the bass kicked in, and the Vegas are pumpin'
Quick to the point, to the point, no faking
Cooking MCs like a pound of bacon
Burning them they ain't quick and nimble
I go crazy when I hear a cymbal
And a hi hat with a souped up tempo
I'm on a roll and it's time to go solo
Rollin' in my 5.0
With my ragtop down so my hair can blow
The girlies on standby, waving just to say, "Hi!"
Did you stop? No, I just drove by
Kept on pursuing to the next stop
I busted a left and I'm heading to the next block
That block was dead Yo
So I continued to A1A Beachfront Ave.

Girls were hot wearing less than bikinis
Rockman lovers driving Lamborghinis
Jealous 'cause I'm out getting mine
Shay with a gauge and Vanilla with a nine
Ready for the chumps on the wall
The chumps acting ill because they're so full of "Eight Ball"
Gunshots ranged out like a bell
I grabbed my nine, all I heard was shells
Falling on the concrete real fast
Jumped in my car, slammed on the gas
Bumper to bumper, the avenue's packed
I'm trying to get away before the jackers jack
Police on the scene, you know what I mean
They passed me up, confronted all the dope fiends

If there was a problem, yo, I'll solve it
Check out the hook while my DJ revolves it

Ice Ice Baby Vanilla, Ice Ice Baby Vanilla
Ice Ice Baby Vanilla, Ice Ice Baby Vanilla

Take heed, 'cause I'm a lyrical poet
Miami's on the scene just in case you didn't know it
My town, that created all the bass sound
Enough to shake and kick holes in the ground
'Cause my style's like a chemical spill
Feasible rhymes that you can vision and feel
Conducted and formed, this is a hell of a concept
We make it hype and you want to step with this
Shay plays on the fade, slice like a ninja
Cut like a razor blade so fast, other DJs say, "Damn."
If my rhyme was a drug, I'd sell it by the gram
Keep my composure when it's time to get loose
Magnetized by the mic while I kick my juice

If there was a problem, Yo, I'll solve it!
Check out the hook while D-Shay revolves it.

Ice Ice Baby Vanilla, Ice Ice Baby Vanilla
Ice Ice Baby Vanilla, Ice Ice Baby Vanilla

Yo, man, let's get out of here! Word to your mother!

Ice Ice Baby Too cold, Ice Ice Baby Too cold Too cold
Ice Ice Baby Too cold Too cold, Ice Ice Baby Too cold Too cold
"""
LETTER_FREQ = {'\n': 2.8952504879635654, 'y': 2.6675341574495772, 'o': 5.823031880286272, ',': 1.398828887443071,
               ' ': 17.56668835393624, 'v': 1.1711125569290826, 'i': 6.701366297983085, 'p': 1.5289525048796355,
               'l': 4.912166558230319, 'e': 8.295380611581002, 't': 5.790500975927131, "'": 0.9433962264150944,
               's': 3.610930383864672, 'k': 1.5289525048796355, 'c': 3.4482758620689653, '!': 0.16265452179570591,
               'b': 2.47234873129473, 'a': 6.701366297983085, 'r': 2.504879635653871, 'g': 1.594014313597918,
               'h': 3.610930383864672, 'n': 4.4567338972023425, 'd': 2.5699414443721533, 'w': 1.3662979830839297,
               'm': 2.147039687703318, 'f': 0.9108653220559532, '?': 0.06506180871828238, 'u': 1.951854261548471,
               'x': 0.13012361743656475, '.': 0.16265452179570591, 'j': 0.4229017566688354, 'q': 0.06506180871828238,
               'z': 0.09759271307742355, '5': 0.03253090435914119, '0': 0.03253090435914119, '"': 0.1951854261548471,
               '1': 0.03253090435914119, '-': 0.03253090435914119}


def ints_to_hex(ints: [int]) -> str:
	s = ""
	for i in ints:
		s += hex(i)[2:].rjust(4, "0")
	return s


def hex_to_ints(hex_s: str) -> [int]:
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


def zip_bytes(buff0, buff1, default=0) -> [(int, int)]:
	for i in range(max(len(buff0), len(buff1))):
		a = default
		b = default
		if i < len(buff0):
			a = buff0[i]
		if i < len(buff1):
			b = buff1[i]
		yield (a, b)


def xor(a: bytes, b: bytes) -> bytes:
	xor_ints = []
	for ai, bi in zip(a, b):
		xor_ints.append(ai ^ bi)
	return bytes(xor_ints)


def word_dictionary():
	with open("/usr/share/dict/words", "r") as fd:
		return set([word.strip() for word in fd.readlines()])


WORD_DICTIONARY = word_dictionary()


def dictionary_word_count(candidate: BA):
	s = to_str(candidate)
	count = 0
	split = s.split(" ")
	for word in split:
		if word in WORD_DICTIONARY:
			count += 1
	return float(count) / len(split)


def to_str(candidate: BA) -> str:
	return "".join([chr(b) for b in candidate.bytes])


def str_to_ba(i: str) -> BA:
	return BA(i.encode())


VALID_LETTERS = set(string.ascii_letters)


def valid_letter_count_percentage(candidate: BA) -> float:
	count = 0
	for c in candidate.bytes:
		if chr(c) in VALID_LETTERS:
			count += 1
	return float(count) / len(candidate.bytes)


def pad_PKCS7(s: bytes) -> bytes:
	hangover = 16 - (len(s) % 16)
	if hangover != 16:
		s += (chr(16).encode()) * hangover
	return s


def pad8(candidate: BA) -> BA:
	hangover = 8 - (len(candidate) % 8)
	if hangover != 8:
		candidate += BA("0x0") * (hangover / 4)
	return candidate


def realistic_letter_distribution(candidate: BA) -> float:
	# pad candidate to get to a byte valid string so we can convert it
	candidate = pad8(candidate)
	s = to_str(candidate).lower()
	return realistic_letter_distribution_(s)


def realistic_letter_distribution_(s: str) -> float:
	score = 0
	uniq_chars = set(s)
	for c in uniq_chars:
		# number of times c appears in s
		num_c_in_s = len(list(filter(lambda x: x == c, s)))

		# frequency of c in s
		p_c = (num_c_in_s / len(s)) * 100

		if c in LETTER_FREQ:
			error = math.fabs(LETTER_FREQ.get(c) - p_c * 10)
			score -= error
		else:
			score -= 300

	return score / len(uniq_chars)


def hamming_weight(a, b):
	return (a ^ b).count(True)


def xor_cycle_encrypt(key: BA, m: BA) -> BA:
	e = key * math.ceil(float(len(m)) / len(key))
	e = e[:len(m)]

	assert len(e) == len(m)
	return e ^ m


def find_best_key(e: BA) -> chr:
	scores = []
	for c in map(chr, range(256)):
		i = ord(c)
		ks = int((len(e) / 8))
		key = BA(hex(i)) * ks
		if len(key) < len(e):
			key = key * 2

		assert len(key) == len(e), "len(key)=%s len(e)=%s" % (len(key), len(e))
		candidate = (e ^ key)

		scores.append((realistic_letter_distribution(candidate), c))

	best = sorted(scores, key=lambda x: x[0])
	return best[-1][1]


def top_n_decrypt_key(n: int, e: BA) -> [(int, chr, str)]:
	scores = attempt_all_keys(e)
	l = list(reversed(sorted(scores, key=lambda x: x[0])))
	return l[:n]


def best_decrypt_key(e: BA) -> (int, chr, str):
	scores = attempt_all_keys(e)
	l = list(reversed(sorted(scores, key=lambda x: x[0])))
	return l[0]


def attempt_all_keys(e: BA) -> [(int, chr, str, BA)]:
	scores = []
	e = pad8(e)
	for i in range(1, 256):
		if i < 16:
			key = BA(hex(i) * int(len(e) / float(4)))
		else:
			key = BA(hex(i) * int(len(e) / float(8)))

		candidate = (e ^ key)

		scores.append((realistic_letter_distribution(candidate), chr(i), to_str(candidate), candidate, e))

	return scores


def top_n_key_sizes(n: int, e: BA) -> [(int, int)]:
	distances = []
	for guess_key_size in range(1, min(50, len(e.bytes))):
		bs = list(e.cut(guess_key_size * 8))
		if not bs or len(bs) == 1:
			continue
		ds = []
		for i in range(len(bs) - 1):
			b0 = bs[i]
			b1 = bs[i + 1]
			ds.append(hamming_weight(b0, b1) / float(guess_key_size))

		distance = sum(ds) / float(len(ds))
		distances.append((guess_key_size, distance))

	return list(sorted(distances, key=lambda x: x[1]))[:n]


def bytes_to_ba(bs: [int]) -> BA:
	l = []
	for b in bs:
		if b == 0:
			l.append("0x00")
		elif b < 15:
			l.append("0x0" + hex(b))
		else:
			l.append(hex(b))
	i = map(lambda s: s[2:], l)
	s = "0x" + "".join(i)
	return BA(s)


def transpose(e: BA, ks: int) -> [BA]:
	blocks = []
	for i in range(ks):
		ith_blocks = []
		for j in range(i, len(e.bytes), ks):
			b = e.bytes[j]
			ith_blocks.append(b)

		ba = bytes_to_ba(ith_blocks)
		blocks.append(ba)
	return blocks


def rand_n_string(n):
	return "".join([random.choice(string.printable) for _ in range(n)])
