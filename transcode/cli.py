import os
import sys
import click

CONTEXT_SETTINGS = dict(
    auto_envvar_prefix='TRANSCODE',
    help_option_names=['-h', '--help']
)

class Environment(object):
    def __init__(self):
        self.verbose = False
        self.subjects = []

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))

class TranscodeCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('transcode.commands.' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=TranscodeCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_environment
def cli(ctx, verbose):
    stdin = click.get_text_stream('stdin')

    if not stdin.isatty():
        ctx.subjects.append(''.join(stdin.readlines()))
    ctx.verbose = verbose
