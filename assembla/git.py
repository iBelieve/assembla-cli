import os
import subprocess


class Repository(object):
    def __init__(self, path=None):
        self.path = path or os.getcwd()

        self.origin_url = self.run('ls-remote --get-url origin')

        if self.origin_url == 'origin':
            self.origin_url = None

        self.branches = [branch[2:] for branch in self.run('branch').split('\n')]

        self.main_branch = 'develop' if self.has_branch('develop') else 'master'
        self.current_branch = self.run('rev-parse --abbrev-ref HEAD')

    @property
    def has_unstaged_changes(self):
        return subprocess.call(['git', 'diff-index', '--quiet', 'HEAD'], cwd=self.path) == 1

    def has_branch(self, branch):
        return branch in self.branches

    def run(self, command):
        return subprocess.check_output(['git'] + command.split(' '), cwd=self.path,
                                       stderr=subprocess.STDOUT).decode('utf-8').strip()
