import unittest
from click.testing import CliRunner

from transcode.commands import b64

TEST_STRING = 'abc'
TEST_STRING_B64 = 'YWJj'

runner = CliRunner()

class TestTranscodeB64(unittest.TestCase):
	def test_encode(self):
		result = runner.invoke(b64.cli, [TEST_STRING])
		self.assertEqual(result.output, TEST_STRING_B64)

	def test_decode(self):
		result = runner.invoke(b64.cli, ['-r', TEST_STRING_B64])
		self.assertEqual(result.output, TEST_STRING)

	def test_stability(self):
		result = runner.invoke(b64.cli, [TEST_STRING])
		result = runner.invoke(b64.cli, ['-r', result.output])
		self.assertEqual(result.output, TEST_STRING)

if __name__ == '__main__':
	unittest.main()
