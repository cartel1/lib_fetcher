import asyncio
import subprocess
import tempfile
import shutil
import os
import traceback
from libfetch.fetch.git import GitFetch

from libfetch.building.strategy.base_build_strategy import BaseBuildStrategy


class MakeBuildStrategy(BaseBuildStrategy):
    def build(self):
        print(
            f'======== Running make build for library to be downloaded to temp work dir: {self.get_lib_dir_name()} ========')

        # Run make commands within temporary work directory
        current_dir = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_lib_work_dir:
            try:
                # Switch to temporary working directory
                os.chdir(temp_lib_work_dir)

                print(f'Switching to temporary working directory: {temp_lib_work_dir}')

                # Get remote source code repository
                print(
                    f'Cloning source code repo at url {self.get_git_repo_url()} and branch {self.get_git_branch()}')

                git_fetch = GitFetch(self.get_git_repo_url(), branch_name=self.get_git_branch(),
                                     lib_dir_name=self.get_lib_dir_name())

                repo = git_fetch.clone_repo()

                print(
                    f'Retreived source code repo at url {self.get_git_repo_url()} and branch {self.get_git_branch()}')

                # Switch to cloned source code home directory and run make building commands
                os.chdir(self.get_lib_dir_name())

                # Run configure command
                completed_proc = subprocess.run(["./configure"] + self.configure_cmd_args, text=True)

                # Throw exception if return code != 0
                completed_proc.check_returncode()

                # Run make command
                make_args = [self.make_cmd_location] if not self.use_make_install_arg else [self.make_cmd_location] + ["install"]

                completed_proc = subprocess.run(make_args, text=True)

                # Throw exception if return code != 0
                completed_proc.check_returncode()

            except ValueError as ve:
                print(f'make build process called with invalid arguments {ve}')
                traceback.print_exc()

            except OSError as ose:
                print(f'make build process called with unknown executable file {ose}')
                traceback.print_exc()

            except Exception as e:
                print(f'Error occurred while running make build: {e}')
                traceback.print_exc()
            finally:
                os.chdir(current_dir)

    def __init__(self, git_repo_url, git_branch, lib_dir_name, lib_output_dir, /, make_cmd_location=None,
                 configure_cmd_args=[], use_make_install_arg=False):
        super().__init__(git_repo_url, git_branch, lib_dir_name, lib_output_dir)

        self.make_cmd_location = make_cmd_location
        self.configure_cmd_args = configure_cmd_args
        self.use_make_install_arg = use_make_install_arg

# async def main(source_code_home_dir, working_dir):
#     make_build = MakeBuildStrategy(source_code_home_dir, working_dir)
#
#     await asyncio.gather(
#         asyncio.to_thread(make_build.building))
