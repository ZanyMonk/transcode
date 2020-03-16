import re
import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('dec', help='Converts to/from decimal.')
@click.argument('subjects', nargs=-1)
@click.option('-js', '--fromCharCode', 'js', is_flag=True, help='ie. String.fromCharCode(97,98,99) > abc')
@add_common_options
@pass_environment
def cli(ctx, subjects, js):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.echo(click.get_current_context().get_help())
        exit(0)

    if ctx.separator == '':
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
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        subject = ctx.strip_fixes(subject)
        numbers = ctx.split(subject)

        print(''.join([
            chr(int(n)) for n in numbers]), end='')


def encode(ctx):
    first = True
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        dec = ctx.separator.join([str(c) for c in subject])

        if not first:
            print()
        else:
            first = False

        print('{}{}{}'.format(ctx.prefix, dec, ctx.suffix), end='')
