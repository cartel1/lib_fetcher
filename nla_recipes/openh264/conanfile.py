from conans import ConanFile, CMake, tools


class Openh264Conan(ConanFile):
    name = "openh264"
    version = "2.1.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    # build_requires = "nasm/2.15.05"
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/cisco/openh264.git", "openh264v2.1.1")

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        self.run("make")

    def package(self):
        self.pkg_helper.package_all_to_bin_variation_dir(self)

    def package_info(self):
        pass
