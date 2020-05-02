import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('not', help='Inverse every bit.')
@click.argument('subjects', nargs=-1)
@add_common_options
@pass_environment
def cli(ctx, subjects):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

    if ctx.separator == '':
        ctx.separator = ' '

    encode(ctx)


def encode(ctx):
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        ctx.output(bytes([b ^ 0xFF for b in subject]))

