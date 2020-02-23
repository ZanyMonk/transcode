import re
import click
import codecs
from transcode.cli import pass_environment
from transcode.common import add_common_options

@click.command('hex', help='Converts to/from hexadecimal.')
@click.argument('subjects', nargs=-1)
@click.option('-u', '--upper', flag_value=True,
	help='Outputs uppercase hexadecimal')
@click.option('-l', '--lower', 'upper', flag_value=False,
	help='Outputs lowercase hexadecimal (default)')
@add_common_options
@pass_environment
def cli(ctx, subjects, upper):
	ctx.subjects = ctx.subjects + list(subjects)

	if len(ctx.subjects) == 0:
		click.echo(click.get_current_context().get_help())

	if ctx.prefix is None:
		ctx.prefix = '0x'

	if ctx.reverse:
		ctx.separator = r'[^\da-f]+'
		ctx.prefix = r'^(0x|[^\da-f]+)'
		ctx.suffix = r'[^\da-f]+$'

	decode(ctx) if ctx.reverse else encode(ctx, upper)

def decode(ctx):
	for subject in ctx.subjects:
		subject = ctx.strip_fixes(subject)
		subject = ''.join(ctx.split(subject))

		print(codecs.decode(bytes(subject, 'utf-8'), 'hex').decode('utf-8'), end='')

def encode(ctx, upper):
	first = True
	for subject in ctx.subjects:
		hex = codecs.encode(bytes(subject, 'utf-8'), 'hex').decode('utf-8')

		hex = ctx.get_separator().join([
			'{}{}'.format(hex[i], hex[i+1]) for i in range(0, len(hex), 2)
		])

		if upper:
			hex = hex.upper()

		if not first:
			print()
		else:
			first = False

		print('{}{}{}'.format(ctx.get_prefix(), hex, ctx.get_suffix()), end='')

if __name__ == '__main__':
	convert()
