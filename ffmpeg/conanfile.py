from conans import ConanFile, AutoToolsBuildEnvironment, tools


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    build_requires = "yasm/1.3.0"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/FFmpeg/FFmpeg.git", "release/4.3")

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        # tools.replace_in_file("ffmpeg/CMakeLists.txt", "PROJECT(FFmpeg)",
        #                       '''PROJECT(FFmpeg)
        #                         include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        #                         conan_basic_setup()''')

    def build(self):
        auto_tools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)

        auto_tools.libs.append("yasm")
        auto_tools.configure(configure_dir=f"{self.source_folder}")
        auto_tools.make()

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        pass

