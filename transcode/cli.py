import io
import os
import sys
import click
from colorama import Fore, Style

from transcode.environment import Environment
from transcode.common import add_common_options

CONTEXT_SETTINGS = dict(
    auto_envvar_prefix='TRANSCODE',
    help_option_names=['-h', '--help']
)

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'commands')
)


class TranscodeCLI(click.MultiCommand):
    def get_help_option(self, ctx):
        """Returns the help option object."""
        help_options = self.get_help_option_names(ctx)
        if not help_options:
            return

        def show_full_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                fmt = click.HelpFormatter()

                self.format_usage(ctx, fmt)

                opts = []
                for p in self.get_params(ctx):
                    rv = p.get_help_record(ctx)
                    if rv is not None:
                        opts.append(rv)

                with fmt.section('{}Options{}'.format(Style.BRIGHT, Style.RESET_ALL)):
                    fmt.write_dl(opts)

                shown = set([''.join(p.opts) for p in self.get_params(ctx)])
                shown.add('subjects')

                fmt.write_text('')
                fmt.write('{}Commands{}:'.format(Style.BRIGHT, Style.RESET_ALL))
                fmt.indent()
                for name in self.list_commands(ctx):
                    cmd = self.get_command(ctx, name)
                    opts = []
                    for p in cmd.get_params(ctx):
                        rv = p.get_help_record(ctx)
                        if ''.join(p.opts) not in shown and rv is not None:
                            opts.append(rv)

                    if opts:
                        with fmt.section('{}{}{}'.format(Style.BRIGHT, name, Style.RESET_ALL)):
                            fmt.write_dl(opts)
                click.echo(fmt.getvalue())
                exit(0)

        return click.Option(help_options, is_flag=True,
                            is_eager=True, expose_value=False,
                            callback=show_full_help,
                            help='Show this message and exit.')

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
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


def lol():
    print('ok')

@click.command(cls=TranscodeCLI, context_settings=CONTEXT_SETTINGS, options_metavar='',
               subcommand_metavar='COMMAND [command options] <subject>',
               add_help_option=False)
@add_common_options
@pass_environment
def cli(ctx):
    if not sys.stdin.isatty():
        stdin = click.get_binary_stream('stdin')
        bytechunks = iter(lambda: stdin.read(io.DEFAULT_BUFFER_SIZE), b'')

        while True:
            try:
                ctx.subjects.append(next(bytechunks))
            except StopIteration:
                break
        # t = stdin.read()
        # print(len(t))
        # print(t)
        # ctx.subjects.append(t)

# 7801010d00efbfbdefbfbd3543444541444245454632430a16efbfbd0318
