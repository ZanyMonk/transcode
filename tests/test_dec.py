import unittest

from transcode.commands import dec
from abstract_test import AbstractTestTranscodeCommand


class TestTranscodeDec(unittest.TestCase, AbstractTestTranscodeCommand):
    cli = dec.cli
    giberish = 'notdecimal'
    result = '97,98,99'
    encode_args = ['-s', ',']


if __name__ == '__main__':
    unittest.main()
