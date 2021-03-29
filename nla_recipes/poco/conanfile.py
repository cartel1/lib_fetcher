from conans import ConanFile, CMake, tools

import os


class PocoConan(ConanFile):
    name = "poco"
    version = "1.10.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    #requires = "openssl/1.1.1"
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

        self.pkg_helper.clean_conan_cache_by_detected_os_host_and_arch(self, self.name, self.version)
        
    def requirements(self):
        if self.settings.os == "Windows":
            self.requires("openssl/1.1.1j")
        elif self.settings.os == "Macos":
            self.requires("openssl/1.1.1")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/pocoproject/poco.git", "poco-1.10.1-release")
        
    def build(self):
        cmake = CMake(self)
        
        config_args = [f"-DCMAKE_INSTALL_PREFIX={self.pkg_helper.get_bin_export_path(self)}"]
        
        if self.settings.os == "Macos":
            cmake.configure(args=config_args)
            
            cmake.build()
            cmake.install()
        
        elif self.settings.os == "Windows":
            cmake_build = "cmake-build"
        
            tools.mkdir(cmake_build)
            
            with tools.chdir(cmake_build):
                config_args.append('-G')
                config_args.append("Visual Studio 16 2019")
                cmake.configure(args=config_args, cache_build_folder=cmake_build)
            
                cmake.build()
                cmake.install()
            

    def package(self):
        self.pkg_helper.build_macosx_universal_bins(self)

