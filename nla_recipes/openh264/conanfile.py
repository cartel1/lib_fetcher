from conans import ConanFile, tools, AutoToolsBuildEnvironment


class Openh264Conan(ConanFile):
    name = "openh264"
    version = "2.1.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    build_requires = "nasm/2.11.06"
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/cisco/openh264.git", "openh264v2.1.1")

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        autotools.make()

    def package(self):
        self.pkg_helper.package_bins(self, extra_bins=[("h264dec", "bin"), ("h264enc", "bin")])

