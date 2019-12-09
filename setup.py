from setuptools import find_packages, setup

setup(
    name='aoc',
    version='1.0',
    url='https://github.com/RazerM/advent-of-code-2019',
    author='Frazer McLean',
    author_email='frazer@frazermclean.co.uk',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'attrs ~= 19.3',
        'click ~= 7.0',
        'networkx ~= 2.4',
        'python-dotenv >= 0.10.3',
        'requests ~= 2.22',
    ],
    extras_require={
        'test': [
            'pytest ~= 5.0',
        ],
    },
)
