import re
import click
from string import ascii_lowercase
from transcode.cli import pass_environment
from transcode.common import add_common_options, RangeParamType

RANGE = RangeParamType()


@click.command('rot', help='Rotates characters.')
@click.option('-n', '--offset', type=RANGE, default=13, show_default=True, metavar='<int>',
              help='Rotation offset.')
@click.option('-a', '--alpha', 'charset', flag_value='alpha', default=True,
              help='Use alphabet (default)')
@click.option('-A', '--ascii', 'charset', flag_value='ascii',
              help='Use entire ASCII charset')
@click.option('-C', '--charset', 'custom_charset', default=None, metavar='<str>',
              help='Use a custom charset. Overwrites -a and -A')
@add_common_options
@pass_environment
def cli(ctx, offset, charset, custom_charset):
    if len(ctx.subjects) == 0:
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

    if custom_charset is not None:
        charset = custom_charset
    elif charset == 'alpha':
        charset = ascii_lowercase
    elif charset == 'ascii':
        charset = ''.join([chr(i) for i in range(32, 127)])

    if ctx.has_prefix:
        ctx.prefix = '%'

    encode(ctx, offset, charset)


def encode(ctx, offset, charset):
    first = True

    for o in offset:
        for subject in ctx.subjects:
            if isinstance(subject, bytes):
                subject = subject.decode('utf-8', 'replace')

            if charset.islower():
                subject = subject.lower()
            elif charset.isupper():
                subject = subject.upper()

            pattern = re.compile('([{}])'.format(re.escape(charset)), re.IGNORECASE)

            def transform(m):
                p = charset.find(m)

                return charset[(p+o) % len(charset)] if p >= 0 else m

            table = ctx.gen_trans_table(subject, pattern, transform)

            if not first:
                print()
            first = False

            print(ctx.translate(subject, table), end='')
