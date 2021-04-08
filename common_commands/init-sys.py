import argparse
import os
import subprocess

from conans import tools

parser = argparse.ArgumentParser(
    description="Initializes the build system so that packages can be created from NLA conan recipes")

parser.add_argument("profile_name", help="The name of the conan profile to use.",
                    choices=["mac_os_arm64_profile", "mac_os_x86_64_profile",
                             "windows_x86_64_msvc_mingw_msys2_profile", "windows_x86_64_profile"])

args = parser.parse_args()

common_cmd_dir = os.getcwd()
base_dir = os.path.dirname(common_cmd_dir)
nla_recipes_dir = os.path.join(base_dir, "nla_recipes")

print("Initializing system! Please wait...")

completed_process = subprocess.run(
    ["conan", "export", os.path.join(nla_recipes_dir, "nla_pkg_helper")], text=True, stderr=subprocess.STDOUT)
completed_process.check_returncode()

if tools.os_info.is_macos:
    completed_process = subprocess.run(
        ["conan", "create", os.path.join(nla_recipes_dir, "nasm"),
         "nasm/2.11.06@", "--profile",
         os.path.join(base_dir, "conan_profiles", args.profile_name)], text=True, stderr=subprocess.STDOUT)
    completed_process.check_returncode()

    completed_process = subprocess.run(
        ["conan", "create", os.path.join(nla_recipes_dir, "nasm"),
         "nasm/2.15.05@", "--profile",
         os.path.join(base_dir, "conan_profiles", args.profile_name)], text=True, stderr=subprocess.STDOUT)
    completed_process.check_returncode()

completed_process = subprocess.run(
    ["conan", "create", os.path.join(nla_recipes_dir, "zlib"),
     "zlib/1.2.11@", "--profile",
     os.path.join(base_dir, "conan_profiles", args.profile_name)], text=True, stderr=subprocess.STDOUT)
completed_process.check_returncode()

if tools.os_info.is_macos:
    completed_process = subprocess.run(
        ["conan", "create", os.path.join(nla_recipes_dir, "openssl"),
         "--profile",
         os.path.join(base_dir, "conan_profiles", args.profile_name)], text=True, stderr=subprocess.STDOUT)
    completed_process.check_returncode()

completed_process = subprocess.run(
    ["conan", "create", os.path.join(nla_recipes_dir, "depot_tools")], text=True, stderr=subprocess.STDOUT)
completed_process.check_returncode()

print("System successfully initialized! You may proceed with creating packages.")
