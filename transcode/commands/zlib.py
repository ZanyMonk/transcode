import zlib
import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option


@click.command('zlib', help='Compress/decompress zlib encoded data.')
@click.argument('subjects', nargs=-1)
@click.option('-l', '--level', type=int, default=6, metavar='<int>',
              help="""\b
              Compression level. [default: 6]
              0: no compression, 1: best speed, 9: best compression""")
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, subjects, level):
    if level < 0 or level > 9:
        click.get_current_context().fail(
            f'Invalid compression level "{level}".' +
            """\nUse one of these values or a value in between:
    0: no compression
    1: best speed
    .
    6: best speed/compression compromise (default)
    .
    9: best compression
            """
        )

    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        ctx.elog('No input given.')
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

    decode(ctx) if ctx.reverse else encode(ctx, level)


def decode(ctx):
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        try:
            decompressed = zlib.decompress(subject)
        except zlib.error as err:
            ctx.elog(err)
            exit(1)

        ctx.output(decompressed)


def encode(ctx, level):
    first = True
    stdout = click.get_binary_stream('stdout')
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8')

        compressed = zlib.compress(subject, level)

        if not first:
            stdout.write('\n')
        else:
            first = False

        if ctx.has_prefix:
            stdout.write(bytes(ctx.prefix, 'utf-8', 'replace'))

        if ctx.unsafe:
            stdout.write(compressed)
        else:
            print(compressed.decode('utf-8', ctx.decode_mode))

        if ctx.has_prefix:
            stdout.write(bytes(ctx.suffix, 'utf-8', 'replace'))
