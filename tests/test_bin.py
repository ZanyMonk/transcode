import unittest
from click.testing import CliRunner

from transcode.commands import bin

TEST_STRING = 'abc'
TEST_STRING_BIN = '1100001 1100010 1100011'

runner = CliRunner()

class TestTranscodeBin(unittest.TestCase):
	def test_encode(self):
		result = runner.invoke(bin.cli, [TEST_STRING])
		self.assertEqual(result.output, TEST_STRING_BIN)

	def test_decode(self):
		result = runner.invoke(bin.cli, ['-r', 'notbinary{}notbinary'.format(TEST_STRING_BIN)])
		self.assertEqual(result.output, TEST_STRING)

	def test_stability(self):
		result = runner.invoke(bin.cli, [TEST_STRING])
		result = runner.invoke(bin.cli, ['-r', 'notbinary{}notbinary'.format(result.output)])
		self.assertEqual(result.output, TEST_STRING)

if __name__ == '__main__':
	unittest.main()
