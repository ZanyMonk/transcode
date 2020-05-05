import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('xor', help='(un)XOR bytes.')
@click.argument('subjects', nargs=-1)
@click.argument('key', nargs=1)
@click.option('-x', '--hexa', is_flag=True, help="Get key as hexadecimal")
@add_common_options
@pass_environment
def cli(ctx, subjects, key, hexa):
    ctx.subjects = ctx.subjects + list(subjects)

    if len(ctx.subjects) == 0:
        click.get_current_context().fail("Error: Missing argument 'SUBJECT'.")

    if hexa:
        if len(key) > 1 and key[1] == 'x':
            key = key[2:]
        key = bytes.fromhex(key.zfill(2))
    else:
        key = bytes(key, 'utf-8', 'replace')

    if not len(key):
        click.get_current_context().fail("Error: Missing argument 'KEY'.")

    encode(ctx, key)


def encode(ctx, key):
    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        result = bytes([subject[i] ^ key[i % len(key)] for i in range(len(subject))])

        ctx.output(result)
