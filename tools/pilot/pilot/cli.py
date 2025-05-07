from argparse import ArgumentParser
from pathlib import Path
import logging

logger = logging.Logger('fastqmd')

def get_cli_arguments():
    cli = ArgumentParser()
    command  = cli.add_subparsers(help='command', dest='command')

    new = command.add_parser('new')
    render = command.add_parser('render')
    new.add_argument('type', choices=['page', 'project'])
    new.add_argument('new_directory', nargs='?', default=Path.cwd(), type=Path)
    new.add_argument('-replace', action='store_true')
    render.add_argument('filepath', nargs='?', default=Path.cwd(), type=Path)
    
    return cli.parse_args()


def main():
    from pilot.qmd import render
    from pilot.utils.find_root import find_root
    args = get_cli_arguments()
    
    if args.command == 'new':
        if not args.new_directory.is_dir():
            args.new_directory.mkdir()

        if args.type == 'project':
            project_file = args.new_directory / '.fastqmd'
            project_file.open('w').write('')
            raise NotImplemented()
        
        if args.type == 'page':
            render.project_files(
                args.new_directory.resolve(),
                logger,
                replace=args.replace,
                index=True,
                )

    if args.command == 'render':
        root = find_root(Path.cwd())
        if args.filepath.is_dir():
            qmd_files = args.filepath.rglob('*.qmd')
        else:
            qmd_files = [args.filepath]

        for file in qmd_files:
            render.render(file, root=root, logger=logger)



if __name__ == '__main__':
    main()


            