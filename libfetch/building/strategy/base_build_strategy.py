from abc import ABCMeta, abstractmethod, abstractproperty

class BaseBuildStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self, git_repo_url, git_branch, lib_dir_name, lib_output_dir):
        self.git_repo_url = git_repo_url
        self.git_branch = git_branch
        self.lib_dir_name = lib_dir_name
        self.lib_output_dir = lib_output_dir

    @abstractmethod
    def build(self):
        pass

    def get_git_repo_url(self):
        return self.git_repo_url

    def get_git_branch(self):
        return self.git_branch

    def get_lib_dir_name(self):
        return self.lib_dir_name

    def get_lib_output_dir(self):
        return self.lib_output_dir
