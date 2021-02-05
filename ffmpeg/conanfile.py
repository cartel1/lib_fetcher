from conans import ConanFile, tools
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
        print("PATH environment variable: %s" % (tools.get_env("PATH")))
        
        if tools.os_info.is_windows:
            self.run("%s %s %s %s %s" % (os.path.join(self.build_folder, 
                "configure"), "--enable-shared", "--arch=x86_64",
                              "--target-os=win64", "--toolchain=msvc"))
        else:
            self.run("%s %s %s" % (os.path.join(self.build_folder, 
                "configure"), "--enable-shared", "--arch=x86_64"))
            
        self.run("make")

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        pass

