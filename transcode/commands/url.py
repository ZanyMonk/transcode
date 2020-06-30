import re
import click
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option


@click.command('url', help='Converts to/from URL encoding (ie. %5C).')
@click.option('-a', '--all', 'mode', flag_value='all',
              help='Process every character')
@click.option('-A', '--non-ascii', 'mode', flag_value='non-ascii',
              help='Process only non-ASCII characters. Not available in reverse mode.')
@click.option('--default', 'mode', flag_value='default', default=True,
              help='Process reserved and unprintable characters (default)"')
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, mode):
    if len(ctx.subjects) == 0:
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

    if not ctx.has_prefix:
        ctx.prefix = '%'

    if ctx.reverse:
        if ctx.separator == '':
            ctx.separator = r'(?i)[^\da-f]+'

        if ctx.prefix == '':
            ctx.prefix = r'^(?i)(0x|[^\da-f]+)'

        if ctx.suffix == '':
            ctx.suffix = r'(?i)[^\da-f]+$'

    decode(ctx) if ctx.reverse else encode(ctx, mode)


def decode(ctx):
    for subject in ctx.subjects:
        string = subject.decode('utf-8', ctx.decode_mode)
        pattern = re.compile(r'(%[a-f0-9]{2})', re.IGNORECASE)
        table = ctx.gen_trans_table(string, pattern, lambda m: chr(int(m[1:], 16)))

        ctx.output(ctx.translate(string, table))


def encode(ctx, mode):
    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        pattern = r'[!*\'\(\);:@&=+$,/?#\[\]\s"%\.<>\\^_`{|}~£円-]'
        flags = re.IGNORECASE

        if mode == 'all':
            pattern = r'(.)'
            flags |= re.DOTALL
        elif mode == 'non-ascii':
            pattern = r'([^\x00-\x7F])'

        regex = re.compile(pattern, flags)

        def transform(m):
            h = hex(ord(m))[2:]
            h_len = len(h)
            h = h.zfill(h_len + h_len%2)
            return ''.join(['%{}'.format(h[i:i+2]) for i in range(0, h_len, 2)])

        table = ctx.gen_trans_table(subject, regex, transform)

        ctx.output(ctx.translate(subject, table))
