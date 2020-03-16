import zlib
import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('zlib', help='Compress/decompress zlib encoded data.')
@click.argument('subjects', nargs=-1)
@click.option('-l', '--level', type=int, default=6, metavar='<int>', show_default=True,
              help='Compression level. 0: no compression, 1: best speed, 9: best compression')
@add_common_options
@pass_environment
def cli(ctx, subjects, level):
    if level < 0 or level > 9:
        ctx.elog("""Invalid compression level "{}". Use one of these values or a value in between:
        0: no compression
        1: best speed
        .
        6: best speed/compression compromise (default)
        .
        9: best compression""".format(level))
        exit(1)

    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        ctx.elog('No input given.')
        click.echo(click.get_current_context().get_help())
        exit(0)

    decode(ctx) if ctx.reverse else encode(ctx, level)


def decode(ctx):
    stdout = click.get_binary_stream('stdout')
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        try:
            decompressed = zlib.decompress(subject)
        except zlib.error as err:
            ctx.elog(err)
            exit(1)

        if ctx.unsafe:
            stdout.write(decompressed)
        else:
            print(decompressed.decode('utf-8', ctx.decode_mode))


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
