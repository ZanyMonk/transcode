import unittest
from click.testing import CliRunner

from transcode.commands import hex

TEST_STRING = 'abc'
TEST_STRING_HEX = '616263'

runner = CliRunner()

class TestTranscodeHex(unittest.TestCase):
	def test_encode(self):
		result = runner.invoke(hex.cli, ['-P', '', TEST_STRING])
		self.assertEqual(result.output, TEST_STRING_HEX)

	def test_decode(self):
		result = runner.invoke(hex.cli, ['-r', 'nothx{}nothx'.format(TEST_STRING_HEX)])
		self.assertEqual(result.output, TEST_STRING)

	def test_stability(self):
		result = runner.invoke(hex.cli, ['-P', '', TEST_STRING])
		result = runner.invoke(hex.cli, ['-r', 'nothx{}nothx'.format(result.output)])
		self.assertEqual(result.output, TEST_STRING)

if __name__ == '__main__':
	unittest.main()
