import os

from conans import ConanFile, CMake, tools


class LibpngConan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    requires = "zlib/1.2.11"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/glennrp/libpng.git", "v1.6.37")

    def build(self):
        self.run(
            [os.path.join(self.build_folder, "configure"), f"--prefix={self.pkg_helper.get_bin_export_path(self)}"])
        self.run(["make", "install"])

    def package(self):
        self.pkg_helper.build_macosx_universal_bins(self)

