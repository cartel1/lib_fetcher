# from dulwich.repo import Repo
from pygit2 import clone_repository, Repository


class GitFetch:
    """ Retrives library source code from a Git reportsitory """

    def __init__(self, repo_url, /, branch_name=None, lib_dir_name="."):
        self.repo_url = repo_url
        self.branch_name = branch_name
        self.lib_dir_name = lib_dir_name

    def clone_repo(self):
        print(f'Cloning repo at url: {self.repo_url} and checking out branch {self.branch_name} ...')
        # repo = porcelain.clone(self.repo_url, self.lib_dir_name, checkout=True)
        repo = clone_repository(self.repo_url, self.lib_dir_name, checkout_branch=self.branch_name)

        active_branch = self.branch_name if repo and repo.branches[self.branch_name].is_checked_out() else ""

        print(f'Current active branch is: {active_branch}')

        return repo.workdir if repo else ""
