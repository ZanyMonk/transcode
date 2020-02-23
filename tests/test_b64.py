import unittest
from click.testing import CliRunner

from transcode.commands import dec

TEST_STRING = 'abc'
TEST_STRING_DEC = '97,98,99'

runner = CliRunner()

class TestTranscodeDec(unittest.TestCase):
	def test_encode(self):
		result = runner.invoke(dec.cli, ['-s', ',', TEST_STRING])
		self.assertEqual(result.output, TEST_STRING_DEC)

	def test_decode(self):
		result = runner.invoke(dec.cli, ['-r', 'notdecimal{}notdecimal'.format(TEST_STRING_DEC)])
		self.assertEqual(result.output, TEST_STRING)

	def test_stability(self):
		result = runner.invoke(dec.cli, ['-s', ',', TEST_STRING])
		result = runner.invoke(dec.cli, ['-r', 'notdecimal{}notdecimal'.format(result.output)])
		self.assertEqual(result.output, TEST_STRING)

if __name__ == '__main__':
	unittest.main()
