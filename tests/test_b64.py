import unittest

from transcode.commands import b64
from abstract_test import AbstractTestTranscodeCommand


class TestTranscodeB64(unittest.TestCase, AbstractTestTranscodeCommand):
    cli = b64.cli
    result = 'YWJj'


if __name__ == '__main__':
    unittest.main()
