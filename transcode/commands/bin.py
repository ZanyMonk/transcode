import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('bin', help='Converts to/from binary.')
@click.argument('subjects', nargs=-1)
@click.option('-b', '--byte-length', default=8, type=int, metavar='<int>', show_default=True,
              help='Byte length')
@add_common_options
@pass_environment
def cli(ctx, subjects, byte_length):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.echo(click.get_current_context().get_help())
        exit(0)

    if ctx.separator == '':
        ctx.separator = ' '

    if ctx.reverse:
        ctx.separator = r'[^01]+'
        ctx.prefix = r'^[^\d]+'
        ctx.suffix = r'[^\d]+$'

    decode(ctx, byte_length) if ctx.reverse else encode(ctx, byte_length)


def decode(ctx, byte_length):
    stdout = click.get_binary_stream('stdout')
    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        subject = ctx.strip_fixes(subject)
        numbers = ctx.split(subject)

        stdout.write(b''.join([int(n, 2).to_bytes(1, 'big') for n in numbers]))


def encode(ctx, byte_length):
    first = True
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        dec = ctx.separator.join([
            bin(c)[2:].rjust(byte_length, '0') for c in subject
        ])

        if not first:
            print()
        else:
            first = False

        print('{}{}{}'.format(ctx.prefix, dec, ctx.suffix), end='')

