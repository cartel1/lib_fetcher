from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class OpensslConan(ConanFile):
    name = "openssl"
    version = "1.1.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def build_requirements(self):
        if tools.os_info.is_windows:
            if not tools.which("perl"):
                self.build_requires("strawberryperl/5.30.0.1")
                
            self.build_requires("nasm/2.15.05")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/openssl/openssl.git", "OpenSSL_1_1_1-stable")

    def build(self):
        #if self.settings.os == "Macos":
        self.run("%s %s %s" % (os.path.join(self.build_folder, "config"), 
            f"--prefix={self.package_folder}", 
            f"--openssldir={os.path.join(self.package_folder, 'ssl')}"))
        self.run("make")
        self.run("make test")
        self.run("make install")

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join(self.package_folder, "include")]
        self.cpp_info.libdirs = [os.path.join(self.package_folder, "lib")]
        self.cpp_info.bindirs = [os.path.join(self.package_folder, "bin")]
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))
        self.user_info.openssldir = os.path.join(self.package_folder, 'ssl')
        

