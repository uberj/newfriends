from enum import Enum

from ecb_util import ordered_block_counts


class BBoxType(Enum):
	ECB = "ECB"
	CBC = "CBC"


def oracle_guess(mystery_text: bytes) -> BBoxType:
	# Check for plain ECB
	ecb_counts = ordered_block_counts(mystery_text)
	if ecb_counts[0][1] > 1:
		return BBoxType.ECB

	# I feel like a cheat. How do distinguish random data from CBC? Some stats tool?
	return BBoxType.CBC

