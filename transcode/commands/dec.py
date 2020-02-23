import re
import click
from transcode.cli import pass_environment
from transcode.common import add_common_options

@click.command('dec', help='Converts to/from decimal.')
@click.argument('subjects', nargs=-1)
@click.option('-js', '--fromCharCode', 'js', is_flag=True)
@add_common_options
@pass_environment
def cli(ctx, subjects, js):
	ctx.subjects = ctx.subjects + list(subjects)

	if len(ctx.subjects) == 0:
		click.echo(click.get_current_context().get_help())

	if ctx.separator == None:
		ctx.separator = ','

	if js:
		ctx.prefix = 'String.fromCharCode('
		ctx.suffix = ')'

	if ctx.reverse:
		ctx.separator = r'[^\d]+'
		ctx.prefix = r'^(String\.fromCharCode\(|[^\d]+)'
		ctx.suffix = r'(\)|[^\d]+)$'

	decode(ctx) if ctx.reverse else encode(ctx)

def decode(ctx):
	for subject in ctx.subjects:
		subject = ctx.strip_fixes(subject)
		numbers = ctx.split(subject)

		print(''.join([
			chr(int(n)) for n in numbers]), end='')

def encode(ctx):
	first = True
	for subject in ctx.subjects:
		dec = ctx.get_separator().join([str(ord(c)) for c in subject])

		if not first:
			print()
		else:
			first = False

		print('{}{}{}'.format(ctx.get_prefix(), dec, ctx.get_suffix()), end='')

if __name__ == '__main__':
	convert()
