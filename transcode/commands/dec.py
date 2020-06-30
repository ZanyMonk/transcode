import click
from transcode.cli import pass_environment
from transcode.common import add_common_options, add_reverse_option


@click.command('dec', help='Converts to/from decimal.')
@click.option('-js', '--fromCharCode', 'js', is_flag=True, help='ie. String.fromCharCode(97,98,99) > abc')
@add_common_options
@add_reverse_option
@pass_environment
def cli(ctx, js):
    if len(ctx.subjects) == 0:
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

    if not ctx.has_separator:
        ctx.separator = ','

    if js:
        ctx.prefix = 'String.fromCharCode('
        ctx.suffix = ')'

    if ctx.reverse:
        ctx.separator = r'[^\d]+'
        ctx.prefix = r'^(String\.fromCharCode\(|[^\d]+)'
        ctx.suffix = r'(\)|[^\d]+)$'

    decode(ctx) if ctx.reverse else encode(ctx)


def decode(ctx):
    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        subject = ctx.strip_fixes(subject)
        numbers = ctx.split(subject)

        ctx.output(bytes([int(n) for n in numbers]))


def encode(ctx):
    first = True

    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        dec = ctx.separator.join([str(c) for c in subject])

        if not first:
            print()
        else:
            first = False

        print('{}{}{}'.format(ctx.prefix, dec, ctx.suffix), end='')
