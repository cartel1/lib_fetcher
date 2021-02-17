from conans import ConanFile, CMake, tools


class XlntConan(ConanFile):
    name = "xlnt"
    version = "1.5.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/tfussell/xlnt.git", "v1.5.0")

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure(args=[f"-DCMAKE_INSTALL_PREFIX={self.pkg_helper.get_bin_export_path(self)}"])
        cmake.build()
        cmake.install()

    def package(self):
        self.pkg_helper.build_universal_bins_on_macosx_arm64(self)
