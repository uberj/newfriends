from enum import Enum

from util.ecb_util import ordered_block_counts


class BBoxType(Enum):
	ECB = "ECB"
	CBC = "CBC"


def oracle_guess_cipher_type(mystery_text: bytes) -> BBoxType:
	# Check for plain ECB
	# If block sizes is not zero there were dupes at some block size. Its probably ECB or some other block cipher
	sizes = oracle_guess_ecb_block_sizes(mystery_text)
	if sizes:
		return BBoxType.ECB

	# I feel like a cheat. How do distinguish random data from CBC? Some stats tool?
	return BBoxType.CBC


def oracle_guess_ecb_block_sizes(mystery_text: bytes) -> [int]:
	"""
	Return the best guesses of block sizes for a given string of ECB encrypted text.
	Best is at 0th array index
	:param mystery_text: ECB encrypted byte string
	:return: List of good block sizes. 0th index is best
	"""
	sizes = []
	for i in reversed(range(4, 10)):
		potential_block_size = 2 ** i
		dupe_block_counts = ordered_block_counts(mystery_text, potential_block_size)
		non_trivial_counts = filter(lambda x_dupe_count: x_dupe_count[1] > 1, dupe_block_counts)
		total_dupe_count = sum(map(lambda x_dupe_count: x_dupe_count[1], non_trivial_counts))
		if dupe_block_counts[0][1] > 1:
			sizes.append((total_dupe_count, potential_block_size))

	sorted_counts = reversed(sorted(sizes, key=lambda dupe_count_x: dupe_count_x[0]))
	just_sizes = map(lambda x_block_size: x_block_size[1], sorted_counts)
	return list(just_sizes)
