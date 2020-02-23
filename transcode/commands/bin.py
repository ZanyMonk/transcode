import re
import click
from transcode.cli import pass_environment
from transcode.common import add_common_options

@click.command('bin', help='Converts to/from binary.')
@click.argument('subjects', nargs=-1)
@click.option('-b', '--byte-length', default=7, type=int)
@add_common_options
@pass_environment
def cli(ctx, subjects, byte_length):
	ctx.subjects = ctx.subjects + list(subjects)

	if len(ctx.subjects) == 0:
		click.echo(click.get_current_context().get_help())

	if ctx.separator is None:
		ctx.separator = ' '

	if ctx.reverse:
		ctx.separator = r'[^\d]+'
		ctx.prefix = r'^[^\d]+'
		ctx.suffix = r'[^\d]+$'

	decode(ctx, byte_length) if ctx.reverse else encode(ctx, byte_length)

def decode(ctx, byte_length):
	for subject in ctx.subjects:
		subject = ctx.strip_fixes(subject)
		numbers = ctx.split(subject)

		print(''.join([
			chr(int(n, 2)) for n in numbers]), end='')

def encode(ctx, byte_length):
	first = True
	for subject in ctx.subjects:
		dec = ctx.get_separator().join([
			bin(ord(c))[2:].rjust(byte_length, '0') for c in subject
		])

		if not first:
			print()
		else:
			first = False

		print('{}{}{}'.format(ctx.get_prefix(), dec, ctx.get_suffix()), end='')

if __name__ == '__main__':
	convert()
