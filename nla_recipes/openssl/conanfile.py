from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class OpensslConan(ConanFile):
    name = "openssl"
    version = "1.1.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    build_policy = "always"
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
        self.run("%s %s" % (os.path.join(self.build_folder, "config"), f"--prefix={self.package_folder}"))
        self.run("make")
        self.run("make test")
        self.run("make install")

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join(self.package_folder, "include")]
        self.cpp_info.libdirs = [os.path.join(self.package_folder, "lib")]
        self.cpp_info.bindirs = [os.path.join(self.package_folder, "bin")]
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))

    def package(self):
        self.pkg_helper.build_universal_bins_on_macosx_arm64(self)
