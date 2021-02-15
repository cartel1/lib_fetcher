from conans import ConanFile, CMake, tools


class PocoConan(ConanFile):
    name = "poco"
    version = "1.10.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    requires = "openssl/1.1.1"
    python_requires = "nla_pkg_helper/1.0"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/pocoproject/poco.git", "poco-1.10.1-release")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        # tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(HelloWorld)",
        #                       '''PROJECT(HelloWorld)
        #     include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        #     conan_basic_setup()''')

    def imports(self):
        self.pkg_helper.import_macos_x86_64_bins(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.pkg_helper.package_all_to_bin_variation_dir(self)
