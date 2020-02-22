import click
import codecs
from transcode.cli import pass_environment

@click.command('dec', help='Converts to/from decimal.')
@click.argument('subjects', nargs=-1)
@click.option('-p', '--prefix', default='')
@click.option('-s', '--suffix', default='')
@click.option('-js', '--fromCharCode', 'js', is_flag=True)
@click.option('-S', '--separator', default=',')
@pass_environment
def cli(ctx, subjects, prefix, suffix, separator, js):
	ctx.subjects = ctx.subjects + list(subjects)

	if js:
		prefix = 'String.fromCharCode('
		suffix = ')'

	if len(ctx.subjects):
		first = True
		for subject in ctx.subjects:
			dec = separator.join([str(ord(c)) for c in subject])

			if not first:
				print()
			else:
				first = False

			print('{}{}{}'.format(prefix, dec, suffix), end='')
	else:
		click.echo(click.get_current_context().get_help())

if __name__ == '__main__':
	convert()
