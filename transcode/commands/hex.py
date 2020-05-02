import click
import codecs
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option


@click.command('hex', short_help='Converts to/from hexadecimal.')
@click.argument('subjects', nargs=-1)
@click.option('-C', '--upper', flag_value=True,
              help='Outputs uppercase hexadecimal')
@click.option('-c', '--lower', 'upper', flag_value=False,
              help='Outputs lowercase hexadecimal (default)')
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, subjects, upper):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

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

        subject = ''.join(ctx.split(ctx.strip_fixes(subject)))
        decoded = codecs.decode(bytes(subject, 'utf-8'), 'hex').decode('utf-8', ctx.decode_mode)

        ctx.output(decoded)


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
