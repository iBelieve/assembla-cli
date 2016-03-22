import click
from .space import AssemblaSpace


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url_or_branch')
def apply(url_or_branch):
    '''Apply a merge request'''
    space().apply_merge_request()


@cli.command('merge-request')
def merge_request():
    '''Create a new merge request'''
    space().merge_request()


def space():
    return AssemblaSpace()
