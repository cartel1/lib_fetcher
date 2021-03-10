import os
import shutil
from distutils.dir_util import copy_tree

from conans import ConanFile, tools


class LibzmqConan(ConanFile):
    name = "libzmq"
    version = "4.3.4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)

    def configure(self):
        if self.settings.os == "Macos":
            self.settings.os.version = "10.10"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    @property
    def zmq_folder_name(self):
        return "zeromq-%s" % self.version

    def source(self):
        suffix = ".zip" if tools.os_info.is_windows else ".tar.gz"
        zmq_zip_name = "%s%s" % (self.zmq_folder_name, suffix)

        suffix = ".zip"
        zmq_zip_name = "%s%s" % (self.zmq_folder_name, suffix)
        zmq_url = "https://github.com/zeromq/libzmq/releases/download/v4.3.4/%s" % zmq_zip_name

        self.output.info("Downloading zmq: %s" % zmq_url)

        tools.download(zmq_url, zmq_zip_name)
        tools.unzip(zmq_zip_name, self.source_folder, keep_permissions=True)

        if not tools.os_info.is_windows:
            copy_tree(os.path.join(self.source_folder, self.zmq_folder_name), self.source_folder)
            shutil.rmtree(os.path.join(self.source_folder, self.zmq_folder_name), ignore_errors=True)

        os.remove(zmq_zip_name)

    def build(self):
        cmd_args = [os.path.join(self.build_folder, "configure"),
                    f"--prefix={self.pkg_helper.get_bin_export_path(self)}"]

        self.pkg_helper.append_shared_build_option(self, cmd_args)

        self.run([cmd_arg for cmd_arg in cmd_args])
        self.run(["make", "install"])

    def package(self):
        self.pkg_helper.build_macosx_universal_bins(self)
