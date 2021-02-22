import os
import subprocess
import traceback
from enum import Enum

from conans import ConanFile, tools


class ConanPackageHelper:
    class ArchVariations(Enum):
        WIN10_X86_64_VARIATION = "win10_x86_64"
        MACOSX_ARM64_VARIATION = "macosx_arm64"
        MACOSX_X86_64_VARIATION = "macosx_x86_64"
        MACOSX_UNIVERSAL_VARIATION = "macosx_universal"

    def import_macos_x86_64_bins(self):
        self.output.info("Running the imports function...")

        if self.get_bin_variation() == self.ArchVariations.MACOSX_ARM64_VARIATION.value:
            self.output.info(
                "Build is currently on a %s platform. Will import any related %s binaries if found to create "
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

        return bin_variation

    def get_bin_export_path(self, make_dir=False):
        bin_dir = os.path.join(self.package_folder, self.get_bin_variation())

        if make_dir:
            os.makedirs(bin_dir, exist_ok=True)

        return bin_dir

    def package_bins(self, extra_bins=None):
        self.package_all_bins_to_bin_variation_dir(extra_bins)
        self.build_macosx_universal_bins()

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

    def _bin_key_func(self, bin_path_mod_time_tup):
        mod_time_key = None

        if bin_path_mod_time_tup:
            mod_time_key = bin_path_mod_time_tup[1]

        return mod_time_key

    def get_latest_bin_variation_pkg_path(self, bin_variation):
        bin_var_path = ""
        pkg_paths = []

        if bin_variation:
            for root, dirs, files in os.walk(os.path.dirname(self.package_folder)):
                for bin_dir in dirs:
                    if bin_dir == bin_variation:
                        bin_var_path = os.path.join(root, bin_dir)
                        pkg_paths.append((bin_var_path, os.path.getmtime(bin_var_path)))
                        break

            if pkg_paths:
                pkg_paths.sort(key=self._bin_key_func, reverse=True)
                bin_var_path = pkg_paths[0][0]

        return bin_var_path

    def build_macosx_universal_bins(self):
        macosx_arm64_bin_var_path = self.get_latest_bin_variation_pkg_path(
            self.ArchVariations.MACOSX_ARM64_VARIATION.value)
        macosx_x86_64_bin_var_path = self.get_latest_bin_variation_pkg_path(
            self.ArchVariations.MACOSX_X86_64_VARIATION.value)

        universal_file = None
        bin_entries_count = 0

        if len(macosx_x86_64_bin_var_path) > 0 and len(macosx_arm64_bin_var_path) > 0:
            self.output.info("Will attempt to generate universal binaries.")

            for root, dirs, files in os.walk(macosx_arm64_bin_var_path):
                for bin_sub_dir in dirs:
                    if bin_sub_dir in ["lib", "bin"]:
                        try:
                            with os.scandir(os.path.join(root, bin_sub_dir)) as bin_entry_iter:
                                for bin_entry in bin_entry_iter:
                                    if bin_entry.is_file():
                                        x86_64_file = os.path.join(macosx_x86_64_bin_var_path, bin_sub_dir,
                                                                   bin_entry.name)

                                        arm64_file = os.path.join(macosx_arm64_bin_var_path, bin_sub_dir,
                                                                  bin_entry.name)

                                        universal_file = os.path.join(macosx_arm64_bin_var_path,
                                                                      self.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value,
                                                                      bin_sub_dir,
                                                                      bin_entry.name)

                                        if not os.path.exists(os.path.dirname(universal_file)):
                                            os.makedirs(os.path.dirname(universal_file))

                                        self.output.info("|| --> Generating universal binary: %s" % universal_file)
                                        self.output.info("--> Using %s file %s" %
                                                         (self.ArchVariations.MACOSX_ARM64_VARIATION.value,
                                                          arm64_file))
                                        self.output.info("--> Using %s file %s" % (
                                            self.ArchVariations.MACOSX_X86_64_VARIATION.value,
                                            x86_64_file))

                                        try:
                                            self.run("lipo -create -output %s %s %s" % (universal_file, arm64_file,
                                                                                        x86_64_file))
                                            bin_entries_count += 1

                                        except Exception:
                                            self.output.info("Error occurred while running lipo!")
                                            traceback.print_exc()
                                            continue

                                        self.output.info(
                                            "!! --> Successfully generated universal binary: %s" % universal_file)
                        except OSError as ose:
                            self.output.info("Error occurred while generating universal binary files: %s" % ose)
                            traceback.print_exc()

                        except Exception as e:
                            self.output.info("Error occurred while running build helper: %s" % e)
                            traceback.print_exc()

            self.output.info(
                "Completed universal binaries creation. %d bin entries were created in directory %s" %
                (bin_entries_count, os.path.join(macosx_arm64_bin_var_path,
                                                 self.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value)))

    def clean_conan_cache_by_detected_os_host_and_arch(self, pkg_name, pkg_version, remote=None):
        local_clean_cache_cmd = ["conan", "remove", f"{pkg_name}/{pkg_version}@", "-s", "-f", "-t", "-q",
                                 f"os={tools.detected_os()} AND arch={tools.detected_architecture()}"]
        self.output.info("Clearing package cache...")
        subprocess.run([cmd_opt for cmd_opt in local_clean_cache_cmd], text=True, stderr=subprocess.STDOUT)

        if remote:
            remote_clean_cache_cmd = local_clean_cache_cmd + ["-r", remote]

            subprocess.run([cmd_opt for cmd_opt in remote_clean_cache_cmd], text=True, stderr=subprocess.STDOUT)

        self.output.info("Package cache cleared...")


class Pkg(ConanFile):
    name = "nla_pkg_helper"
    version = "1.0"
