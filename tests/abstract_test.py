from click.testing import CliRunner

runner = CliRunner()


class AbstractTestTranscodeCommand(object):
    gibberish = ''
    subject = 'abc'
    encode_args = []
    decode_args = []

    def add_gibberish(self, subject):
        return '{}{}{}'.format(self.gibberish, subject, self.gibberish)

    def test_encode(self):
        result = runner.invoke(self.cli, [self.subject] + self.encode_args)
        self.assertEqual(result.output, self.result)

    def test_decode(self):
        result = runner.invoke(self.cli, [self.add_gibberish(self.result), '-r'] + self.decode_args)
        self.assertEqual(result.output, self.subject)

    def test_stability(self):
        result = runner.invoke(self.cli, [self.subject] + self.encode_args)
        result = runner.invoke(self.cli, [self.add_gibberish(result.output), '-r'] + self.decode_args)
        self.assertEqual(result.output, self.subject)


if __name__ == '__main__':
    print('This script is not supposed to be ran on its own.')
    exit(1)
