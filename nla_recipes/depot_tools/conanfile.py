import os
import shutil

from conans import ConanFile, tools
from distutils.dir_util import copy_tree


class DepotToolsConan(ConanFile):
    name = "depot_tools"
    version = "cci.20201009"
    settings = "os", "compiler", "build_type", "arch"
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None
    
    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper
        
        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)

    def source(self):
        git = tools.Git()
        git.clone("https://chromium.googlesource.com/chromium/tools/depot_tools.git")
        
    def package(self):
        self.copy("*", src=self.source_folder, dst=self.package_folder, keep_path=True)
        
        if tools.os_info.is_windows:
            with tools.environment_append({"PATH": [self.source_folder]}):
                self.run(["gclient.bat"])

    def package_info(self):
        self.cpp_info.bindirs = [self.package_folder]
        self.env_info.DEPOT_TOOLS_PATH.append(self.package_folder)
