from conans import ConanFile, tools


class DepotToolsConan(ConanFile):
    name = "depot_tools"
    version = "cci.20201009"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        git = tools.Git()
        git.clone("https://chromium.googlesource.com/chromium/tools/depot_tools")

    def package(self):
        self.copy("*", src=self.source_folder, dst=self.package_folder, keep_path=True)

    def package_info(self):
        self.cpp_info.bindirs = [self.package_folder]
        self.env_info.PATH.append(self.package_folder)
