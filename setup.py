from pathlib import Path
from setuptools import setup, find_packages


root = Path(__file__).resolve().parent
template = root / 'web_qmd' / 'template'
requirements = (root / 'requirements.txt').read_text().split('\n')
name = u'web_qmd'
version = '1'
description = "Website Tooling"
setup_args = dict(
    name=name,
    version=version,
    description=description,
    author='Jo-L Swear',
    author_email='joelsewhere@gmail.com',
    license='MIT',
    url='http://github.com/joelsewhere/web_qmd',
    packages=find_packages(),
    package_data={
    'template': ['*'],
    'config': ['*'],
    'content': ['*'],
    'files': ['*'],
    'src': ['*']
    },
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': ['web_qmd=web_qmd.cli:main']
    },
)

if __name__ == "__main__":
    setup(**setup_args)