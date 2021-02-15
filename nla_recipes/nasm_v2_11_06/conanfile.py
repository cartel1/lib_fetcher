from conans import ConanFile, tools
from distutils.dir_util import copy_tree
import os
import shutil


class NasmConan(ConanFile):
    name = "nasm"
    version = "2.11.06"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

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
        # "https://www.nasm.us/pub/nasm/releasebuilds/2.11.06/nasm-2.11.06.tar.gz"
        tools.download("http://www.nasm.us/"
                       "pub/nasm/releasebuilds/"
                       "%s/%s" % (self.version, nasm_zip_name), nasm_zip_name)
        self.output.info("Downloading nasm: "
                         "http://www.nasm.us/pub/nasm/releasebuilds"
                         "/%s/%s" % (self.version, nasm_zip_name))
        tools.unzip(nasm_zip_name, self.source_folder)
        copy_tree(os.path.join(self.source_folder, self.nasm_folder_name), self.source_folder)
        shutil.rmtree(os.path.join(self.source_folder, self.nasm_folder_name), ignore_errors=True)
        # os.unlink(nasm_zip_name)

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        self.run("%s" % (os.path.join(self.build_folder, "configure")))
        self.run("make")

    def package(self):
        self.pkg_helper.package_all_to_bin_variation_dir(self)
