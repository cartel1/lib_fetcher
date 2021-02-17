from conans import ConanFile, CMake, tools
import os


class ZlibConan(ConanFile):
    name = "zlib"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    build_policy = "always"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def set_version(self):
        # Read the value from 'version.txt' if it is not provided in the command line
        self.version = self.version or tools.load(os.path.join(self.recipe_folder, "version.txt"))

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/madler/zlib.git", f"v{self.version}")

    def build(self):
        cmake = CMake(self)
        cmake.configure(args=[f"-DCMAKE_INSTALL_PREFIX={self.package_folder}"])
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join(self.package_folder, "include")]
        self.cpp_info.libdirs = [os.path.join(self.package_folder, "lib")]
        self.cpp_info.bindirs = [os.path.join(self.package_folder, "bin")]


