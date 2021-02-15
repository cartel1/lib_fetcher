from conans import ConanFile, tools
import os


class OpensslConan(ConanFile):
    name = "openssl"
    version = "1.1.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def build_requirements(self):
        if tools.os_info.is_windows and not tools.which("perl"):
            self.build_requires("strawberryperl/5.30.0.1")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/openssl/openssl.git", "OpenSSL_1_1_1-stable")

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        self.run("%s" % (os.path.join(self.build_folder, "config")))
        self.run("make")

    def package(self):
        self.pkg_helper.package_all_to_bin_variation_dir(self)
