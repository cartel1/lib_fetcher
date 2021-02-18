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

    def import_macos_x86_64_bins(self):
        # Look for macosx_x86_64 pkg bins and copy them to temp directory relative this conanfile.py file
        # and which has the the name as that of the source pkg.
        print("Running the imports function...")

        if self.get_bin_variation() == self.ArchVariations.MACOSX_ARM64_VARIATION.value:
            print("Build is currently on a %s platform. Will import any related %s binaries if found to create "
                  "universal "
                  " binaries" % self.ArchVariations.MACOSX_ARM64_VARIATION.value,
                  self.ArchVariations.MACOSX_X86_64_VARIATION.value)

            self.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.lib",
                      dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                      root_package=self.name,
                      folder=True, keep_path=True)

            self.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.dll",
                      dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "bin"),
                      root_package=self.name,
                      folder=True, keep_path=True)

            self.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.so",
                      dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                      root_package=self.name,
                      folder=True, keep_path=True)

            self.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.dylib",
                      dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                      root_package=self.name,
                      folder=True, keep_path=True)

            self.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.a",
                      dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                      root_package=self.name,
                      folder=True, keep_path=True)

            self.copy(f"*{self.ArchVariations.MACOSX_X86_64_VARIATION.value}*.exe",
                      dst=os.path.join(self.ArchVariations.MACOSX_X86_64_VARIATION.value, "bin"),
                      root_package=self.name,
                      folder=True, keep_path=True)

    @staticmethod
    def check_conan_file(conan_file):
        if not conan_file or issubclass(conan_file.__class__, ConanFile):
            raise Exception(
                "Bad paramter type %s! Paramter must be a non null ConanFile object." % conan_file.__class__)

    def get_bin_variation(self):
        bin_variation = ""

        if not tools.cross_building(self, "Windows", "x86_64"):
            bin_variation = self.ArchVariations.WIN10_X86_64_VARIATION.value

        elif not tools.cross_building(self, "Macos", "armv8"):
            bin_variation = self.ArchVariations.MACOSX_ARM64_VARIATION.value

        elif not tools.cross_building(self, "Macos", "x86_64"):
            bin_variation = self.ArchVariations.MACOSX_X86_64_VARIATION.value

        # elif tools.cross_building(conan_file, "Macos", "x86_64"):
        #     bin_variation = self.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value

        return bin_variation

    def get_bin_export_path(self, make_dir=False):
        bin_dir = os.path.join(self.package_folder, self.get_bin_variation())

        if make_dir:
            os.makedirs(bin_dir, exist_ok=True)

        return bin_dir

    def package_bins(self, extra_bins=None):
        self.package_all_bins_to_bin_variation_dir(extra_bins)
        self.build_universal_bins_on_macosx_arm64()

    def package_all_bins_to_bin_variation_dir(self, extra_bins=None):
        bin_variation = self.get_bin_variation()

        self.copy("*.h", dst=os.path.join(bin_variation, "include"), keep_path=False)
        self.copy("*.lib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.copy("*.dll", dst=os.path.join(bin_variation, "bin"), keep_path=False)
        self.copy("*.exe", dst=os.path.join(bin_variation, "bin"), keep_path=False)
        self.copy("*.so", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.copy("*.dylib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        self.copy("*.a", dst=os.path.join(bin_variation, "lib"), keep_path=False)

        if extra_bins:
            for file_pattern, src_dir in extra_bins:
                self.copy(file_pattern, dst=os.path.join(bin_variation, src_dir), keep_path=False)

    def build_universal_bins_on_macosx_arm64(self):
        bin_variation = self.get_bin_variation()

        if bin_variation == self.ArchVariations.MACOSX_ARM64_VARIATION.value:
            # Iterate through each matching binary file in each macosx_arm64 and macosx_x86_64 directory and create
            # universal bin files

            print("Will attempt to generate universal binaries.")

            temp_x86_64_bin_dir = os.path.join(self.recipe_folder,
                                               self.ArchVariations.MACOSX_X86_64_VARIATION.value)

            shutil.rmtree(temp_x86_64_bin_dir, ignore_errors=True)

            for bin_sub_dir in ["lib", "bin"]:
                try:
                    with os.scandir(os.path.join(temp_x86_64_bin_dir, bin_sub_dir)) as bin_entry_iter:
                        for bin_entry in bin_entry_iter:
                            if os.path.exists(os.path.join(self.package_folder, bin_variation, bin_sub_dir,
                                                           bin_entry.name)):

                                arm64_file = os.path.join(self.package_folder, bin_variation, bin_sub_dir,
                                                          bin_entry.name)

                                x86_64_file = os.path.join(temp_x86_64_bin_dir, bin_sub_dir, bin_entry.name)

                                universal_file = os.path.join(self.package_folder, bin_variation,
                                                              self.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value,
                                                              bin_sub_dir,
                                                              bin_entry.name)

                                if not os.path.exists(os.path.dirname(universal_file)):
                                    os.makedirs(os.path.dirname(universal_file))

                                print("|| --> Generating universal binary: %s", universal_file)
                                print("--> Using %s file %s", self.ArchVariations.MACOSX_ARM64_VARIATION.value,
                                      arm64_file)
                                print("--> Using %s file %s", self.ArchVariations.MACOSX_X86_64_VARIATION.value,
                                      x86_64_file)

                                self.run("lipo -create -output %s %s $s", universal_file, arm64_file,
                                         x86_64_file)

                                print("!! --> Successfully generated universal binary: %s", universal_file)
                except OSError as ose:
                    print("Error occured while generating universal binary files: %s", ose)
                    traceback.print_exc()

                except Exception as e:
                    print("Error occurred while running build helper: %s", e)
                    traceback.print_exc()

                finally:
                    uni_bins_export_folder = os.path.join(self.package_folder, bin_variation)

                    print("Completed universal binaries creation. %d entries were created in directory %s",
                          len(os.listdir(uni_bins_export_folder)), uni_bins_export_folder)
                    shutil.rmtree(temp_x86_64_bin_dir, ignore_errors=True)


class Pkg(ConanFile):
    name = "nla_pkg_helper"
    version = "1.0"
