import unittest

from transcode.commands import hex
from abstract_test import AbstractTestTranscodeCommand


class TestTranscodeHex(unittest.TestCase, AbstractTestTranscodeCommand):
    cli = hex.cli
    giberish = 'not_hx'
    result = '616263'
    encode_args = ['-P', '']


if __name__ == '__main__':
    unittest.main()
