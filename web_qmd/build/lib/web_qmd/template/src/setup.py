from pathlib import Path
from setuptools import setup, find_packages


root = Path(__file__).resolve().parent
requirements = (root / 'requirements.txt').read_text().split('\n')

name = u'src'
version = '1'
description = "src"
setup_args = dict(
    name=name,
    version=version,
    description=description,
    author='Jo-L Swear',
    author_email='joelsewhere@gmail.com',
    license='MIT',
    url='http://github.com/joelsewhere/web_qmd',
    packages=find_packages(),
    install_requires=requirements,
)

if __name__ == "__main__":
    setup(**setup_args)