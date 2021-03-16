from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    requires = "zlib/1.2.11"
    build_requires = "nasm/2.15.05"
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/FFmpeg/FFmpeg.git", "release/4.3")

    def build(self):
        self._build_bin_variation()

    def package(self):
        self.pkg_helper.build_macosx_universal_bins(self)

    def _build_bin_variation(self):
        autotools = AutoToolsBuildEnvironment(self)
        
        autotools.include_paths = self.deps_cpp_info["zlib"].include_paths
        autotools.library_paths = self.deps_cpp_info["zlib"].lib_paths + self.deps_cpp_info["zlib"].bin_paths

        cmd_args = [f"--prefix={self.pkg_helper.get_bin_export_path(self)}", "--enable-shared",
                    "--enable-gpl", "--disable-outdev=sdl",
                    "--enable-runtime-cpudetect", "--disable-bzlib",
                    "--disable-libfreetype", "--disable-libopenjpeg"]

        if tools.os_info.is_macos:
            if self.settings.arch == "armv8":
                cmd_args = cmd_args + ["--arch=arm64"]

            elif self.settings.arch == "x86_64":
                cmd_args = cmd_args + ["--arch=x86_64"]

        autotools.configure(args=cmd_args)
        autotools.install()

