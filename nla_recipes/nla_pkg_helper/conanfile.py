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

    conan_file = None

    @classmethod
    def import_macos_x86_64_bins(cls, conan_file):
        # Look for macosx_x86_64 pkg bins and copy them to temp directory relative this conanfile.py file
        # and which has the the name as that of the source pkg.
        print("Running the imports function...")

        if cls.get_bin_variation(conan_file) == cls.ArchVariations.MACOSX_ARM64_VARIATION.value:
            print("Build is currently on a %s platform. Will import any related % binaries if found to create universal"
                  " binaries" % cls.ArchVariations.MACOSX_ARM64_VARIATION.value,
                  cls.ArchVariations.MACOSX_X86_64_VARIATION.value)

            conan_file.copy(f"*{cls.ArchVariations.MACOSX_X86_64_VARIATION.value}*.lib",
                            dst=os.path.join(cls.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                            root_package=conan_file.name,
                            folder=True, keep_path=True)

            conan_file.copy(f"*{cls.ArchVariations.MACOSX_X86_64_VARIATION.value}*.dll",
                            dst=os.path.join(cls.ArchVariations.MACOSX_X86_64_VARIATION.value, "bin"),
                            root_package=conan_file.name,
                            folder=True, keep_path=True)

            conan_file.copy(f"*{cls.ArchVariations.MACOSX_X86_64_VARIATION.value}*.so",
                            dst=os.path.join(cls.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                            root_package=conan_file.name,
                            folder=True, keep_path=True)

            conan_file.copy(f"*{cls.ArchVariations.MACOSX_X86_64_VARIATION.value}*.dylib",
                            dst=os.path.join(cls.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                            root_package=conan_file.name,
                            folder=True, keep_path=True)

            conan_file.copy(f"*{cls.ArchVariations.MACOSX_X86_64_VARIATION.value}*.a",
                            dst=os.path.join(cls.ArchVariations.MACOSX_X86_64_VARIATION.value, "lib"),
                            root_package=conan_file.name,
                            folder=True, keep_path=True)

            conan_file.copy(f"*{cls.ArchVariations.MACOSX_X86_64_VARIATION.value}*.exe",
                            dst=os.path.join(cls.ArchVariations.MACOSX_X86_64_VARIATION.value, "bin"),
                            root_package=conan_file.name,
                            folder=True, keep_path=True)

    @classmethod
    def check_conan_file(cls, conan_file):
        if not conan_file or isinstance(conan_file, ConanFile):
            raise Exception("Bad paramter! Paramter must be a non null ConanFile object.")

    @classmethod
    def build_bin_variation(cls, conan_file, enable_shared=False):
        print("PATH environment variable: %s" % (tools.get_env("PATH")))
        print("AS environment variable: %s" % (tools.get_env("AS")))

        if tools.os_info.is_windows:
            if enable_shared:
                conan_file.run("%s %s %s %s %s" % (os.path.join(conan_file.build_folder,
                                                                "configure"), "--enable-shared", "--arch=x86_64",
                                                   "--target-os=win64", "--toolchain=msvc"))
            else:
                conan_file.run("%s %s %s %s" % (os.path.join(conan_file.build_folder,
                                                             "configure"), "--arch=x86_64",
                                                "--target-os=win64", "--toolchain=msvc"))
        if tools.os_info.is_macos:
            more_params = ""

            if conan_file.settings.arch == "armv8":
                more_params = "--disable-x86asm --arch=arm64"

            elif conan_file.settings.arch == "x86_64":
                more_params = "--arch=x86_64"

            if enable_shared:
                conan_file.run(
                    "%s %s %s" % (os.path.join(conan_file.build_folder, "configure"), "--enable-shared",
                                  more_params))
            else:
                conan_file.run(
                    "%s %s" % (os.path.join(conan_file.build_folder, "configure"),
                               more_params))

        conan_file.run("make")

    @classmethod
    def get_bin_variation(cls, conan_file):
        bin_variation = ""

        if not tools.cross_building(conan_file, "Windows", "x86_64"):
            bin_variation = cls.ArchVariations.WIN10_X86_64_VARIATION.value

        elif not tools.cross_building(conan_file, "Macos", "armv8"):
            bin_variation = cls.ArchVariations.MACOSX_ARM64_VARIATION.value

        elif not tools.cross_building(conan_file, "Macos", "x86_64"):
            bin_variation = cls.ArchVariations.MACOSX_X86_64_VARIATION.value

        # elif tools.cross_building(conan_file, "Macos", "x86_64"):
        #     bin_variation = cls.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value

        return bin_variation

    @classmethod
    def get_bin_export_path(cls, conan_file, make_dir=False):
        bin_dir = os.path.join(conan_file.package_folder, cls.get_bin_variation(conan_file))

        if make_dir:
            os.makedirs(bin_dir, exist_ok=True)

        return bin_dir

    @classmethod
    def package_bins(cls, conan_file, extra_bins=[]):
        cls.package_all_bins_to_bin_variation_dir(conan_file, extra_bins)
        cls.build_universal_bins_on_macosx_arm64(conan_file)

    @classmethod
    def package_all_bins_to_bin_variation_dir(cls, conan_file, extra_bins=[]):
        bin_variation = cls.get_bin_variation(conan_file)

        conan_file.copy("*.h", dst=os.path.join(bin_variation, "include"), keep_path=False)
        conan_file.copy("*.lib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        conan_file.copy("*.dll", dst=os.path.join(bin_variation, "bin"), keep_path=False)
        conan_file.copy("*.exe", dst=os.path.join(bin_variation, "bin"), keep_path=False)
        conan_file.copy("*.so", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        conan_file.copy("*.dylib", dst=os.path.join(bin_variation, "lib"), keep_path=False)
        conan_file.copy("*.a", dst=os.path.join(bin_variation, "lib"), keep_path=False)

        if extra_bins:
            for file_pattern, src_dir in extra_bins:
                conan_file.copy(file_pattern, dst=os.path.join(bin_variation, src_dir), keep_path=False)

    @classmethod
    def build_universal_bins_on_macosx_arm64(cls, conan_file):
        bin_variation = cls.get_bin_variation(conan_file)

        if bin_variation == cls.ArchVariations.MACOSX_ARM64_VARIATION.value:
            # Iterate through each matching binary file in each macosx_arm64 and macosx_x86_64 directory and create
            # universal bin files

            print("Will attempt to generate universal binaries.")

            temp_x86_64_bin_dir = os.path.join(conan_file.recipe_folder,
                                               cls.ArchVariations.MACOSX_X86_64_VARIATION.value)

            shutil.rmtree(temp_x86_64_bin_dir, ignore_errors=True)

            for bin_sub_dir in ["lib", "bin"]:
                try:
                    with os.scandir(os.path.join(temp_x86_64_bin_dir, bin_sub_dir)) as bin_entry_iter:
                        for bin_entry in bin_entry_iter:
                            if os.path.exists(os.path.join(conan_file.package_folder, bin_variation, bin_sub_dir,
                                                           bin_entry.name)):

                                arm64_file = os.path.join(conan_file.package_folder, bin_variation, bin_sub_dir,
                                                          bin_entry.name)

                                x86_64_file = os.path.join(temp_x86_64_bin_dir, bin_sub_dir, bin_entry.name)

                                universal_file = os.path.join(conan_file.package_folder, bin_variation,
                                                              cls.ArchVariations.MACOSX_UNIVERSAL_VARIATION.value,
                                                              bin_sub_dir,
                                                              bin_entry.name)

                                if not os.path.exists(os.path.dirname(universal_file)):
                                    os.makedirs(os.path.dirname(universal_file))

                                print("|| --> Generating universal binary: %s", universal_file)
                                print("--> Using %s file %s", cls.ArchVariations.MACOSX_ARM64_VARIATION.value,
                                      arm64_file)
                                print("--> Using %s file %s", cls.ArchVariations.MACOSX_X86_64_VARIATION.value,
                                      x86_64_file)

                                conan_file.run("lipo -create -output %s %s $s", universal_file, arm64_file,
                                               x86_64_file)

                                print("!! --> Successfully generated universal binary: %s", universal_file)
                except OSError as ose:
                    print("Error occured while generating universal binary files: %s", ose)
                    traceback.print_exc()

                except Exception as e:
                    print("Error occurred while running build helper: %s", e)
                    traceback.print_exc()

                finally:
                    uni_bins_export_folder = os.path.join(conan_file.package_folder, bin_variation)

                    print("Completed universal binaries creation. %d entries were created in directory %s",
                          len(os.listdir(uni_bins_export_folder)), uni_bins_export_folder)
                    shutil.rmtree(temp_x86_64_bin_dir, ignore_errors=True)


class Pkg(ConanFile):
    name = "nla_pkg_helper"
    version = "1.0"
