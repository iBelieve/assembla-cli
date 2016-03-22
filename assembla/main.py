import click
from .space import AssemblaSpace


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url_or_branch')
def apply(url_or_branch):
    '''Apply a merge request'''
    space().apply_merge_request(url_or_branch)


@cli.command('merge-request')
def merge_request():
    '''Create a new merge request'''
    space().make_merge_request()


@cli.command('review')
def review():
    '''Review open merge requests'''
    space().view_merge_requests()


@cli.command('tickets')
def tickets():
    '''View open tickets'''
    space().view_tickets()


@cli.command('new-ticket')
def new_ticket():
    '''Open a new ticket'''
    space().new_ticket()


def space():
    return AssemblaSpace()
