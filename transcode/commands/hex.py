import click
import codecs
from transcode.cli import pass_environment

@click.command('hex', help='Converts to/from hexadecimal.')
@click.argument('subjects', nargs=-1)
@click.option('-p', '--prefix', default='0x')
@click.option('-s', '--suffix', default='')
@click.option('-S', '--separator', default='')
@pass_environment
def cli(ctx, subjects, prefix, suffix, separator):
	ctx.subjects = ctx.subjects + list(subjects)

	if len(ctx.subjects):
		first = True
		for subject in ctx.subjects:
			hex = codecs.encode(bytes(subject, 'utf-8'), 'hex').decode('utf-8')

			if len(separator):
				hex = separator.join(['{}{}'.format(hex[i], hex[i+1]) for i in range(0, len(hex), 2)])

			if not first:
				print()
			else:
				first = False

			print('{}{}{}'.format(prefix, hex, suffix), end='')
	else:
		click.echo(click.get_current_context().get_help())

if __name__ == '__main__':
	convert()
