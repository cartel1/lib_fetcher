from conans import ConanFile, tools
from nla.package.utils.build_helper import ConanPackageHelper
import os


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/FFmpeg/FFmpeg.git", "release/4.3")

    def build(self):
        self._build_bin_variation()

    def _build_bin_variation(self):
        print("PATH environment variable: %s" % (tools.get_env("PATH")))
        print("AS environment variable: %s" % (tools.get_env("AS")))

        if tools.os_info.is_windows:
            self.run("%s %s %s %s %s" % (os.path.join(self.build_folder,
                                                      "configure"), "--enable-shared", "--arch=x86_64",
                                         "--target-os=win64", "--toolchain=msvc"))
        if tools.os_info.is_macos:
            more_params = ""

            if self.settings.arch == "armv8":
                more_params = "--disable-x86asm --arch=arm64"

            elif self.settings.arch == "x86_64":
                more_params = "--arch=x86_64"

            self.run("%s %s %s" % (os.path.join(self.build_folder, "configure"), "--enable-shared", more_params))

        self.run("make")

    def _get_bin_variation(self):
        bin_variation = ""

        if not tools.cross_building(self, "Windows", "x86_64"):
            bin_variation = "win10_x86_64"

        elif not tools.cross_building(self, "Macos", "armv8"):
            bin_variation = "macosx_arm64"

        elif not tools.cross_building(self, "Macos", "x86_64"):
            bin_variation = "macosx_x86_64"

        elif tools.cross_building(self, "Macos", "x86_64"):
            bin_variation = "macosx_universal"

        return bin_variation

    def package(self):
        bin_variation = self._get_bin_variation()

        self.copy("*.h", dst=os.path.join(bin_variation, "include"), keep_path=False)
        self.copy("*.lib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.copy("*.dll", dst=os.path.join(bin_variation, "bin"), keep_path=False)
        self.copy("*.so", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.copy("*.dylib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.copy("*.a", dst=os.path.join(bin_variation, "lib"), keep_path=False)

    def package_info(self):
        pass
