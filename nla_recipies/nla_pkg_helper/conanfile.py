import traceback
import os
import shutil
from enum import Enum
from conans import ConanFile, tools


class ConanPackageHelper:
    class ArchVariations(Enum):
        WIN10_X86_64_VARIATION = "win10_x86_64"
        MACOSX_ARM64_VARIATION = "macosx_arm64"
        MACOSX_X86_64_VARIATION = "macosx_x86_64"
        MACOSX_UNIVERSAL_VARIATION = "macosx_universal"

    def __init__(self, conan_file: ConanFile):
        self.conan_file = conan_file

    def check_conan_file(self):
        if not self.conan_file or isinstance(self.conan_file, ConanFile):
            raise Exception("Bad paramter! Paramter must be a non null ConanFile object.")

    def build_bin_variation(self):
        print("PATH environment variable: %s" % (tools.get_env("PATH")))
        print("AS environment variable: %s" % (tools.get_env("AS")))

        if tools.os_info.is_windows:
            self.conan_file.run("%s %s %s %s %s" % (os.path.join(self.conan_file.build_folder,
                                                                 "configure"), "--enable-shared", "--arch=x86_64",
                                                    "--target-os=win64", "--toolchain=msvc"))
        if tools.os_info.is_macos:
            more_params = ""

            if self.conan_file.settings.arch == "armv8":
                more_params = "--disable-x86asm --arch=arm64"

            elif self.conan_file.settings.arch == "x86_64":
                more_params = "--arch=x86_64"

            self.conan_file.run(
                "%s %s %s" % (os.path.join(self.conan_file.build_folder, "configure"), "--enable-shared", more_params))

        self.conan_file.run("make")

    def get_bin_variation(self):
        bin_variation = ""

        if not tools.cross_building(self.conan_file, "Windows", "x86_64"):
            bin_variation = self.ArchVariations.WIN10_X86_64_VARIATION.value

        elif not tools.cross_building(self.conan_file, "Macos", "armv8"):
            bin_variation = self.ArchVariations.MACOSX_ARM64_VARIATION.value

        elif not tools.cross_building(self.conan_file, "Macos", "x86_64"):
            bin_variation = self.ArchVariations.MACOSX_X86_64_VARIATION.value

        elif tools.cross_building(self.conan_file, "Macos", "x86_64"):
            bin_variation = self.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value

        return bin_variation

    def package_all_to_bin_variation_dir(self):
        bin_variation = self.get_bin_variation()

        self.conan_file.copy("*.h", dst=os.path.join(bin_variation, "include"), keep_path=False)
        self.conan_file.copy("*.lib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.conan_file.copy("*.dll", dst=os.path.join(bin_variation, "bin"), keep_path=False)
        self.conan_file.copy("*.so", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.conan_file.copy("*.dylib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.conan_file.copy("*.a", dst=os.path.join(bin_variation, "lib"), keep_path=False)

        self._build_universal_bins_on_macosx_arm64()

    def _build_universal_bins_on_macosx_arm64(self):
        bin_variation = self.get_bin_variation()

        if bin_variation == "macosx_arm64":
            # Look for macosx_x86_64 pkg bins and copy them to temp directory relative this conanfile.py file
            # and which has the the name as that of the source pkg.
            self.conan_file.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.lib",
                                 dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                                 rootpackage=self.conan_file.name,
                                 folder=True, keep_path=True)

            self.conan_file.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.dll",
                                 dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "bin"),
                                 rootpackage=self.conan_file.name,
                                 folder=True, keep_path=True)

            self.conan_file.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.so",
                                 dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                                 rootpackage=self.conan_file.name,
                                 folder=True, keep_path=True)

            self.conan_file.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.dylib",
                                 dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                                 rootpackage=self.conan_file.name,
                                 folder=True, keep_path=True)

            self.conan_file.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.a",
                                 dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                                 rootpackage=self.conan_file.name,
                                 folder=True, keep_path=True)

            # Iterate through each matching binary file in each macosx_arm64 and macosx_x86_64 directory and create
            # universal bin files

            temp_x86_64_bin_dir = os.path.join(self.conan_file.recipe_folder,
                                               self.ArchVariations.MACOSX_X86_64_VARIATION.value)

            shutil.rmtree(temp_x86_64_bin_dir, ignore_errors=True)

            for bin_sub_dir in ["lib", "bin"]:
                try:
                    with os.scandir(os.path.join(temp_x86_64_bin_dir, bin_sub_dir)) as bin_entry_iter:
                        for bin_entry in bin_entry_iter:
                            if os.path.exists(os.path.join(self.conan_file.package_folder, bin_variation, bin_sub_dir,
                                                           bin_entry.name)):

                                arm64_file = os.path.join(self.conan_file.package_folder, bin_variation, bin_sub_dir,
                                                          bin_entry.name)

                                x86_64_file = os.path.join(temp_x86_64_bin_dir, bin_sub_dir, bin_entry.name)

                                universal_file = os.path.join(self.conan_file.package_folder, bin_variation,
                                                              self.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value,
                                                              bin_sub_dir,
                                                              bin_entry.name)

                                if not os.path.exists(os.path.dirname(universal_file)):
                                    os.makedirs(os.path.dirname(universal_file))

                                self.conan_file.run("lipo -create -output %s %s $s", universal_file, arm64_file,
                                                    x86_64_file)
                except OSError as ose:
                    print("Error occured while generating universal binary files: %s", ose)
                    traceback.print_exc()

                except Exception as e:
                    print("Error occurred while running build helper: %s", e)
                    traceback.print_exc()

                finally:
                    shutil.rmtree(temp_x86_64_bin_dir, ignore_errors=True)


class Pkg(ConanFile):
    name = "nla_pkg_helper"
    version = "1.0"
