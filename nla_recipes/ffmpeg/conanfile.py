from conans import ConanFile, tools


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        self.build_requires("yasm/1.3.0")

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/FFmpeg/FFmpeg.git", "release/4.3")

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        self.pkg_helper.build_bin_variation(self, enable_shared=True)

    def package(self):
        self.pkg_helper.package_all_to_bin_variation_dir(self)

    def package_info(self):
        pass
