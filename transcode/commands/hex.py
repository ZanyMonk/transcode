import click
import codecs
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('hex', short_help='Converts to/from hexadecimal.')
@click.argument('subjects', nargs=-1)
@click.option('-C', '--upper', flag_value=True,
              help='Outputs uppercase hexadecimal')
@click.option('-c', '--lower', 'upper', flag_value=False,
              help='Outputs lowercase hexadecimal (default)')
@add_common_options
@pass_environment
def cli(ctx, subjects, upper):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.echo(click.get_current_context().get_help())
        exit(0)

    if not ctx.has_prefix:
        ctx.prefix = '0x'

    if ctx.reverse:
        if ctx.separator == '':
            ctx.separator = r'(?i)[^\da-f]+'

        if ctx.prefix == '':
            ctx.prefix = r'^(?i)(0x|[^\da-f]+)'

        if ctx.suffix == '':
            ctx.suffix = r'(?i)[^\da-f]+$'

    decode(ctx) if ctx.reverse else encode(ctx, upper)


def decode(ctx):
    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        subject = ctx.strip_fixes(subject)
        subject = ''.join(ctx.split(subject))

        print(codecs.decode(bytes(subject, 'utf-8'), 'hex').decode('utf-8', ctx.decode_mode), end='')


def encode(ctx, upper):
    first = True
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', ctx.decode_mode)

        result = codecs.encode(subject, 'hex').decode('utf-8')

        result = ctx.separator.join([
            '{}{}'.format(result[i], result[i + 1]) for i in range(0, len(result), 2)
        ])

        if upper:
            result = result.upper()

        if not first:
            print()
        else:
            first = False

        print('{}{}{}'.format(ctx.prefix, result, ctx.suffix), end='')
