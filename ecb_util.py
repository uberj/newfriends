def find_needle(haystack: [str]) -> str:
	counts = map(lambda s: (s, count_identical_blocks(s)), haystack)
	return pick_highest_dupe_count(counts)


def count_identical_blocks(s: bytes):
	counts = {}
	for i in range(0, len(s), 16):
		c = "".join(map(chr, s[i:i+16]))
		counts.setdefault(c, 0)
		counts[c] += 1
	return counts


def ordered_block_counts(s: bytes):
	counts = count_identical_blocks(s)
	l = sorted(counts.items(), key=lambda c: c[1])
	return list(reversed(l))


def pick_highest_dupe_count(counts):
	block_counts = list(reversed(sorted(counts, key=lambda c: max(c[1].values()))))
	return block_counts[0]

