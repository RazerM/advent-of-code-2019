#!/usr/bin/env python3
import os

import click
import requests
from dotenv import load_dotenv

from aoc import get_solver

INPUT_URL = 'https://adventofcode.com/2019/day/{day}/input'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('day', type=click.IntRange(min=1, max=25))
@click.argument('file', type=click.File('r'), default='-')
@click.option(
    '-v', '--verbose',
    count=True,
    help=(
        'Typically -v will print some progress information, -vvv may spam the '
        'screen with puzzle state.'
    ),
)
def run(day, file, verbose):
    """If FILE is not passed, stdin is used instead."""
    try:
        solve = get_solver(day)
    except KeyError:
        raise click.UsageError('Unimplemented!')

    solve(file, verbose)


@cli.command()
@click.argument('day', type=click.IntRange(min=1, max=25))
@click.argument('file', type=click.File('x'))
def download(day, file):
    """Download input for DAY to FILE. Will not overwrite."""
    load_dotenv()
    try:
        cookies = dict(session=os.environ['AOC_SESSION'])
    except KeyError:
        raise click.UsageError(
            'Set AOC_SESSION environment variable (or add to .env file)'
        )
    response = requests.get(INPUT_URL.format(day=day), cookies=cookies)
    response.raise_for_status()
    file.write(response.text)


if __name__ == '__main__':
    cli()
