import argparse

from . import commands


# Add new commands here
COMMANDS = [
    'init',
    'commit',
    'add',
    'status'
    ]


def main():
    args = args_parser()
    if args.command in COMMANDS: 
        args.execute(args)
        

def args_parser():
    # Input parser, add sub args and default functions

    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    init_parser = sub_parsers.add_parser('init', help='new repo')
    init_parser.set_defaults(execute=commands.init)

    commit_parser = sub_parsers.add_parser('commit', help='commit all staged files')
    commit_parser.set_defaults(execute=commands.commit)

    test = sub_parsers.add_parser('add', help='stage your files')
    test.set_defaults(execute=commands.add)
    test.add_argument('files', nargs='+')

    status_parser = sub_parsers.add_parser('status', help='show status of files')
    status_parser.set_defaults(execute=commands.status)

    return parser.parse_args()


