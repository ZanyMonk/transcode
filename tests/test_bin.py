import unittest

from transcode.commands import bin
from abstract_test import AbstractTestTranscodeCommand


class TestTranscodeBin(unittest.TestCase, AbstractTestTranscodeCommand):
	cli = bin.cli
	giberish = 'not_binary'
	result = '1100001 1100010 1100011'

if __name__ == '__main__':
	unittest.main()
