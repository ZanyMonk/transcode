import click
import codecs
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('b64', help='Converts to/from base64.')
@click.argument('subjects', nargs=-1)
@add_common_options
@pass_environment
def cli(ctx, subjects):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.echo(click.get_current_context().get_help())

    decode(ctx) if ctx.reverse else encode(ctx)


def decode(ctx):
    for subject in ctx.subjects:
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', 'replace')

        subject = ctx.strip_fixes(subject)

        print(codecs.decode(bytes(subject, 'utf-8'), 'base64').decode('utf-8'), end='')


def encode(ctx):
    first = True
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        b64 = codecs.encode(subject, 'base64').decode('utf-8')[:-1]

        if not first:
            print()
        else:
            first = False

        print('{}{}{}'.format(ctx.prefix, b64, ctx.suffix), end='')
