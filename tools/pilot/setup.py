from pathlib import Path
from setuptools import setup, find_packages


root = Path(__file__).resolve().parent
requirements = (root / 'pilot' / 'requirements.txt').read_text().split('\n')

name = u'pilot'
version = '1'
description = "Website Tooling"
setup_args = dict(
    name=name,
    version=version,
    description=description,
    author='Jo-L Collins',
    author_email='joelsewhere@gmail.com',
    license='MIT',
    url='http://github.com/joelsewhere/pilot',
    packages=find_packages(),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': ['pilot=pilot.cli:main']
    },
)

if __name__ == "__main__":
    setup(**setup_args)