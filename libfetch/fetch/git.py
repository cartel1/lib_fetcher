from dulwich.repo import Repo
import dulwich.porcelain as porcelain
import tempfile


class GitFetch:
    """ Retrives library source code from a Git reportsitory """

    def __init__(self, repo_url):
        self.repo_url = repo_url

    def clone_repo(self, working_dir):
        working_dir_path = working_dir if working_dir else "."
        repo = porcelain.clone(self.repo_url, working_dir_path)

        return repo

    def build_repo(selfself, repo, target_lib_output_dir):
        pass