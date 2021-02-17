from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    build_requires = "nasm/2.15.05"
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/FFmpeg/FFmpeg.git", "release/4.3")

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        self._build_bin_variation()

    def package(self):
        self.pkg_helper.build_universal_bins_on_macosx_arm64(self)

    def _build_bin_variation(self):
        autotools = AutoToolsBuildEnvironment(self)

        autotools.libs.append("nasm")

        cmd_args = [f"--prefix={self.pkg_helper.get_bin_export_path(self)}", "--enable-shared"]

        if tools.os_info.is_windows:
            cmd_args = cmd_args + ["--arch=x86_64", "--target-os=win64", "--toolchain=msvc"]

        elif tools.os_info.is_macos:
            if self.settings.arch == "armv8":
                cmd_args = cmd_args + ["--arch=arm64"]

            elif self.settings.arch == "x86_64":
                cmd_args = cmd_args + ["--arch=x86_64"]

        autotools.configure(args=[cmd_option for cmd_option in cmd_args])
        autotools.install()

