from conans import ConanFile, tools, AutoToolsBuildEnvironment
from distutils.dir_util import copy_tree
import os
import shutil


class NasmConan(ConanFile):
    name = "nasm"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def set_version(self):
        # Read the value from 'version.txt' if it is not provided in the command line
        self.version = self.version or tools.load(os.path.join(self.recipe_folder, "version.txt"))

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def build_requirements(self):
        if tools.os_info.is_windows and not tools.which("perl"):
            self.build_requires("strawberryperl/5.30.0.1")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    @property
    def nasm_folder_name(self):
        return "nasm-%s" % self.version

    def source(self):
        suffix = ".zip" if tools.os_info.is_windows else ".tar.gz"
        nasm_zip_name = "%s%s" % (self.nasm_folder_name, suffix)

        # "https://www.nasm.us/pub/nasm/releasebuilds/<version>/nasm-<version>.tar.gz"
        tools.download("http://www.nasm.us/"
                       "pub/nasm/releasebuilds/"
                       "%s/%s" % (self.version, nasm_zip_name), nasm_zip_name)
        self.output.info("Downloading nasm: "
                         "http://www.nasm.us/pub/nasm/releasebuilds"
                         "/%s/%s" % (self.version, nasm_zip_name))
        tools.unzip(nasm_zip_name, self.source_folder)

        if not tools.os_info.is_windows:
            copy_tree(os.path.join(self.source_folder, self.nasm_folder_name), self.source_folder)
            shutil.rmtree(os.path.join(self.source_folder, self.nasm_folder_name), ignore_errors=True)

        os.remove(nasm_zip_name)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        autotools.configure(configure_dir=self.build_folder)
        autotools.install()

    def package_info(self):
        self.cpp_info.bindirs = [os.path.join(self.package_folder, "bin")]
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))
