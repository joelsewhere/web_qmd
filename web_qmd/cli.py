from argparse import ArgumentParser
from pathlib import Path
import logging
from shutil import copytree, copy

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
    from web_qmd import render
    from web_qmd.utils import find_root
    args = get_cli_arguments()
    
    if args.command == 'new':
        root = args.new_directory
        if not root.is_dir():
            root.mkdir()

        if args.type == 'project':
            template = Path(__file__).parent / 'template'
            for path in template.iterdir():
                new_path = root / path.name
                if path.is_dir():
                    copytree(path, new_path)
                else:
                    copy(path, new_path)

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


            