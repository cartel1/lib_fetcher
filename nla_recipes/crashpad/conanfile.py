from conans import ConanFile, tools
import os


class CrashpadConan(ConanFile):
    name = "crashpad"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    python_requires = "nla_pkg_helper/1.0"
    python_requires_extend = "nla_pkg_helper.ConanPackageHelper"
    pkg_helper = None
    out_dir = "out"
    release_dir = "Release"

    def init(self):
        self.pkg_helper = self.python_requires["nla_pkg_helper"].module.ConanPackageHelper

    def build_requirements(self):
        self.build_requires("depot_tools/cci.20201009")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run(f"fetch {self.name}", run_environment=True)

    def build(self):
        with tools.chdir(self.name):
            output_dir = os.path.join(self.out_dir, self.release_dir)
            arch_map = {self.pkg_helper.ArchVariations.WIN10_X86_64_VARIATION.value: "x64",
                        self.pkg_helper.ArchVariations.MACOSX_ARM64_VARIATION.value: "arm64",
                        self.pkg_helper.ArchVariations.MACOSX_X86_64_VARIATION.value: "x64"}

            self.run(f"gn gen {output_dir}")
            tools.save(os.path.join(self.build_folder, self.name, output_dir, "args.gn"),
                       'target_cpu=\"%s\"' % arch_map[self.pkg_helper.get_bin_variation(self)], append=True)
            self.run(f"ninja -C {output_dir}")

    def package(self):
        src_bins = os.path.join(self.build_folder, self.name, self.out_dir, self.release_dir)

        self.pkg_helper.package_all_bins_to_bin_variation_dir(self, bin_src=src_bins)

        bin_variation = self.pkg_helper.get_bin_variation(self)

        self.copy("*", dst=os.path.join(bin_variation, "bin"),
                  src=src_bins,
                  excludes=("*.h", "*.lib", "*.dll", "*.exe", "*.so", "*.dylib", "*.a",
                            "*.cpp", "*.c", "*.html", "*.js", "*.ninja", "*.gyp", "*.cc",
                            "*.py", "*.abilist", "*.inc", "*.exp", "*.m", "*.rst", "*.o", "*.stamp", "*.gn", "*.d",
                            "*.ninja_deps", "*.ninja_log"),
                  keep_path=False)

        self._rename_static_libs_with_prefix("libcrashpad")

        self.pkg_helper.build_macosx_universal_bins(self)

    def _rename_static_libs_with_prefix(self, new_lib_prefix):
        bin_variation = self.pkg_helper.get_bin_variation(self)

        libs_path = os.path.join(self.package_folder, bin_variation, "lib")

        if libs_path and os.path.exists(libs_path):
            for root, dirs, files in os.walk(os.path.join(libs_path)):
                for lib_file in files:
                    if lib_file.startswith("lib"):
                        tools.rename(os.path.join(libs_path, lib_file),
                                     os.path.join(libs_path, lib_file.replace("lib", new_lib_prefix, 1)))
