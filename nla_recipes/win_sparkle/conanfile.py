from conans import ConanFile, tools, MSBuild
from conans.errors import ConanInvalidConfiguration


class WinSparkleConan(ConanFile):
    name = "win_sparkle"
    version = "0.7.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("This library is only needed for Windows")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()

        git.clone("https://github.com/vslavik/winsparkle.git")
        git.checkout("v0.7.0", submodule="recursive")

    def build(self):
        msbuild = MSBuild(self)

        msbuild.build("WinSparkle.sln")

    def package(self):
        self.pkg_helper.package_bins(self)

