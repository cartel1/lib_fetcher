from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

import os


class WinSparkleConan(ConanFile):
    name = "win_sparkle"
    version = "0.7.0"
    settings = "os", "compiler", "build_type", "arch"
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)

    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("This library is only needed for Windows")
            
    @property
    def win_sparkle_folder_name(self):
        return "WinSparkle-%s" % self.version

    def source(self):
        suffix = ".zip"
        win_sparkle_zip_name = "%s%s" % (self.win_sparkle_folder_name, suffix)

        # "https://github.com/vslavik/winsparkle/releases/download/v0.7.0/WinSparkle-0.7.0.zip"
        tools.download("https://github.com/vslavik/winsparkle/"
            "releases/download/v%s/%s" % (self.version, win_sparkle_zip_name), win_sparkle_zip_name)
        self.output.info("Downloading nasm: "
                         "http://www.nasm.us/pub/nasm/releasebuilds"
                         "/%s/%s" % (self.version, win_sparkle_zip_name))
        tools.unzip(win_sparkle_zip_name, self.source_folder)

        os.remove(win_sparkle_zip_name)

    def build(self):
        # Remove x86 release folder to leave only x64 release folder
        tools.rmdir(os.path.join(self.build_folder, "Release"))

    def package(self):
        self.pkg_helper.package_bins(self)

