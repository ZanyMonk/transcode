import re
import click
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option


@click.command('url', help='Converts to/from URL encoding (ie. %5C).')
@click.argument('subjects', nargs=-1)
@click.option('-a', '--all', 'process_all', flag_value=True, default=True,
              help='Process every character')
@click.option('-A', '--non-ascii', 'process_all', flag_value=False,
              help='Process only non-ASCII characters. Not available in reverse mode. (default)')
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, subjects, process_all):
    ctx.subjects = ctx.subjects + list(subjects)

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

    decode(ctx) if ctx.reverse else encode(ctx, process_all)


def decode(ctx):
    for subject in ctx.subjects:
        string = subject.decode('utf-8', ctx.decode_mode)
        pattern = re.compile(r'(%[a-f0-9]{2})', re.IGNORECASE)
        table = ctx.gen_trans_table(string, pattern, lambda m: chr(int(m[1:], 16)))

        ctx.output(ctx.translate(string, table))


def encode(ctx, process_all):
    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        if process_all:
            pattern = re.compile(r'(.)', re.IGNORECASE | re.DOTALL)
        else:
            pattern = re.compile(r'([^\x00-\x7F])', re.IGNORECASE)

        def transform(m):
            h = hex(ord(m))[2:]
            l = len(h)
            h = h.zfill(l + l%2)
            return ''.join(['%{}'.format(h[i:i+2]) for i in range(0, l, 2)])

        table = ctx.gen_trans_table(subject, pattern, transform)

        if process_all:
            for c in subject:
                print(table[c], end='')
        else:
            print(ctx.translate(subject, table), end='')
