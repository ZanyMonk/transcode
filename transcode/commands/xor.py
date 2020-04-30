import click
from sys import exit
from transcode.cli import pass_environment
from transcode.common import add_common_options


@click.command('xor', help='(un)XOR bytes.')
@click.argument('subjects', nargs=-1)
@click.argument('key', nargs=1)
@add_common_options
@pass_environment
def cli(ctx, subjects, key):
    ctx.subjects = ctx.subjects + list(subjects)
    key = bytes(key, 'utf-8', 'replace')

    if len(ctx.subjects) == 0:
        click.echo(click.get_current_context().get_help())
        exit(0)

    encode(ctx, key)


def encode(ctx, key):
    stdout = click.get_binary_stream('stdout')

    for subject in ctx.subjects:
        if isinstance(subject, str):
            subject = bytes(subject, 'utf-8', 'replace')

        result = bytes([subject[i] ^ key[i % len(key)] for i in range(len(subject))])

        if ctx.unsafe:
            stdout.write(result)
        else:
            print(result.decode('utf-8', ctx.decode_mode))

