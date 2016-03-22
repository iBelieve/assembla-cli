import re
import webbrowser
from click import ClickException
from .api import get_merge_request, close_merge_request
from .git import Repository


class AssemblaSpace(Repository):
    def __init__(self, path=None):
        super(AssemblaSpace, self).__init__(path)

        if not self.origin_url:
            raise ClickException('Can\'t identify Assembla repo: no origin found')

        match = re.match(r'git@git\.assembla\.com:([^.]+)(\..*)?\.git', self.origin_url)

        if not match:
            match = re.match(r'https:\/\/git\.assembla\.com\/([^.]+)(\..*)?\.git', self.origin_url)

        if match is not None:
            self.name = match.group(1)
        else:
            raise ClickException('Not inside an Assembla git repo: ' + self.origin_url)

    def open_url(self, url):
        webbrowser.open('https://www.assembla.com/spaces/{}/{}'.format(self.name, url))

    def open_code_url(self, url):
        webbrowser.open('https://www.assembla.com/code/{}/{}'.format(self.name, url))

    def view_merge_requests(self):
        self.open_url('git/merge_requests')

    def view_tickets(self):
        self.open_url('tickets')

    def new_ticket(self):
        self.open_url('tickets/new')

    def make_merge_request(self):
        if self.main_branch == self.current_branch:
            raise ClickException('Currently on the {} branch, cannot open merge request.'
                                 .format(self.main_branch))

        self.open_code_url('git/compare/{}...{}'.format(self.main_branch, self.current_branch))

    def apply_merge_request(self, url_or_branch):
        if self.has_unstaged_changes:
            raise ClickException('Git index must be empty before merging a merge request')

        match = re.match(r'https:\/\/www\.assembla\.com\/spaces\/(.+)\/git\/merge_requests\/(\d+)(\?.+)?',
                         url_or_branch)

        if match:
            space_name = match.group(1)
            merge_id = match.group(2)

            if space_name != self.name:
                raise ClickException('Unable to merge MR from a different Assembla space: ' + space_name)

            merge_request = get_merge_request(self.name, merge_id)

            if merge_request['status'] != 0:
                raise ClickException('This merge request has already been merged or rejected!')

            source_branch = merge_request['source_symbol']
            target_branch = merge_request['target_symbol']
            temp_branch = 'assembla-merge-' + merge_id
        else:
            source_branch = url_or_branch
            target_branch = self.current_branch
            temp_branch = 'assembla-merge-' + source_branch.replace('_', '-').replace('/', '-')

        print('Fetching merge request from ' + source_branch)

        self.run('fetch {} {}'.format(self.origin_url, source_branch))
        self.run('branch -f {} FETCH_HEAD'.format(temp_branch))
        self.run('checkout {}'.format(temp_branch))

        print('Rebasing on top of ' + target_branch)
        self.run('rebase ' + target_branch)

        print('Merging {} onto {}'.format(source_branch, target_branch))
        self.run('checkout ' + target_branch)
        self.run('merge --ff-only ' + temp_branch)

        if merge_request:
            print('Closing merge request')
            close_merge_request(self.name, merge_id)
