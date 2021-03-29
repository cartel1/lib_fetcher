from conans import ConanFile, tools, AutoToolsBuildEnvironment, CMake
import os



class ProtobufConan(ConanFile):
    name = "protobuf"
    version = "3.14.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
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

        git.clone("https://github.com/protocolbuffers/protobuf.git")
        git.checkout("v3.14.0", submodule="recursive")

    def build(self):
        if self.settings.os == "Macos":
            self.run(os.path.join(self.build_folder, "autogen.sh"))

            cmd_args = [f"--prefix={self.pkg_helper.get_bin_export_path(self)}"]

            self.pkg_helper.append_shared_build_option(self, cmd_args)

            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=cmd_args)
            autotools.install
            
        elif self.settings.os == "Windows":
            cmake = CMake(self)
            
            cmake_source = "cmake"
            
            with tools.chdir(cmake_source):
                cmake_build = "build"
        
                tools.mkdir(cmake_build)
                
                with tools.chdir(cmake_build):
                    config_args = [f"-DCMAKE_INSTALL_PREFIX={self.pkg_helper.get_bin_export_path(self)}"]
                    
                    if self.options.shared:
                        config_args.append("-Dprotobuf_BUILD_SHARED_LIBS=ON")
                        
                        cmake.definitions["CXXFLAGS"] = "-DPROTOBUF_USE_DLLS"
                    
                    config_args.append('-G')
                    config_args.append("Visual Studio 16 2019")
                    cmake.configure(args=config_args, source_folder=os.path.join(self.build_folder, cmake_source), 
                        cache_build_folder=os.path.join(self.build_folder, cmake_source, cmake_build))
                
                    cmake.build()
                    cmake.install()

    def package(self):
        self.pkg_helper.build_macosx_universal_bins(self)
