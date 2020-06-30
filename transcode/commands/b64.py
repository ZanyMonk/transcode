import click
import codecs
from binascii import Error as Base64Error
from itertools import permutations
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option

STANDARD_CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
CHARSET_LEN = len(STANDARD_CHARSET)


@click.command('b64', help='Converts to/from base64.')
@click.option('-c', '--charset', help='Custom charset.',
              default=STANDARD_CHARSET, show_default=True)
@click.option('-bf', '--bruteforce', is_flag=True, default=False, help='Try all charset combinations')
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, charset, bruteforce):
    if len(ctx.subjects) == 0:
        click.echo(click.get_current_context().get_help())

    if len(charset) != CHARSET_LEN:
        click.get_current_context().fail(f'Invalid charset length. Please provide a charset of {CHARSET_LEN} items.')

    # if bruteforce:
    #     i = 0
    #     for perm in permutations(charset):
    #         print(i, perm)
    #         i = i + 1
        # trans_tables = [ctx.gen_trans_table(STANDARD_CHARSET, r'.', lambda c: perm[STANDARD_CHARSET.index(c)])
        #                 for perm in permutations(charset)]

    decode(ctx, charset, bruteforce) if ctx.reverse else encode(ctx, charset)


def decode(ctx, charset, bruteforce):
    trans = False
    if charset != STANDARD_CHARSET and not bruteforce:
        trans = True
        trans_table = ctx.gen_trans_table(charset, r'.', lambda c: STANDARD_CHARSET[charset.index(c)])

    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        subject = ctx.strip_fixes(subject)

        if bruteforce:
            for perm in permutations(charset):
                trans_table = ctx.gen_trans_table(''.join(perm), r'.', lambda c: STANDARD_CHARSET[perm.index(c)])
                subject = ctx.translate(subject, trans_table)

                try:
                    decoded = codecs.decode(bytes(subject, 'utf-8'), 'base64')
                    ctx.output(decoded)
                except Base64Error:
                    if ctx.verbosity:
                        ctx.elog('failed decoding b64.')
        else:
            if trans:
                subject = ctx.translate(subject, trans_table)

            try:
                decoded = codecs.decode(bytes(subject, 'utf-8'), 'base64')
                ctx.output(decoded)
            except Base64Error:
                ctx.elog('failed decoding b64.')


def encode(ctx, charset):
    first = True
    trans = False
    if charset != STANDARD_CHARSET:
        trans = True
        trans_table = ctx.gen_trans_table(STANDARD_CHARSET, r'.', lambda c: charset[STANDARD_CHARSET.index(c)])

    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        b64 = codecs.encode(subject, 'base64').decode('utf-8').replace('\n', '')

        if trans:
            b64 = ctx.translate(b64, trans_table)

        if not first:
            print()
        else:
            first = False

        print('{}{}{}'.format(ctx.prefix, b64, ctx.suffix), end='')
