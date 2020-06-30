from io import BufferedReader

import click
import codecs
from sys import exit
from os import path
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option


@click.command('hex', short_help='Converts to/from hexadecimal.')
# @click.argument('subjects', nargs=-1)
@click.option('-C', '--upper', flag_value=True,
              help='Outputs uppercase hexadecimal')
@click.option('-c', '--lower', 'upper', flag_value=False,
              help='Outputs lowercase hexadecimal (default)')
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, upper):
    # ctx.subjects = ctx.subjects + list(subjects)
    # print(ctx)

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

    for subject in ctx.subjects:
        if isinstance(subject, BufferedReader):
            data = subject.readlines()
        else:
            data = subject

        decode(ctx, data) if ctx.reverse else encode(ctx, data, upper)


def decode(ctx, subject):
    if isinstance(subject, bytes):
        subject = subject.decode('utf-8', 'replace')

    subject = ''.join(ctx.split(ctx.strip_fixes(subject)))
    decoded = codecs.decode(bytes(subject, 'utf-8'), 'hex')

    ctx.output(decoded)


def encode(ctx, subject, upper):
    # print(subject)
    if isinstance(subject, str):
        subject = bytes(subject, 'utf-8', ctx.decode_mode)

    # print(subject)

    result = codecs.encode(subject, 'hex').decode('utf-8')

    result = ctx.separator.join([
        '{}{}'.format(result[i], result[i + 1]) for i in range(0, len(result), 2)
    ])

    if upper:
        result = result.upper()

    # if not first:
    #     print()
    # else:
    #     first = False

    print('{}{}{}'.format(ctx.prefix, result, ctx.suffix), end='')
