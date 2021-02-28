import argparse
import os

from nla_utils.CommandUtil import exec_common_cmd

parser = argparse.ArgumentParser(description="Creates packages from NLA conan recipes")

parser.add_argument("recipe_name", help='The name of the recipe. Use "*" (including quotes) for all recipes.')
parser.add_argument("profile_name", help="The name of the conan profile to use.",
                    choices=["mac_os_arm64_profile", "mac_os_x86_64_profile",
                             "windows_x86_64_msvc_mingw_msys2_profile"])
parser.add_argument("-vn", "--version", help="Package version to use if package allows for alternative versions.")

args = parser.parse_args()

common_cmd_dir = os.getcwd()
base_dir = os.path.dirname(common_cmd_dir)
profiles_dir = os.path.join(base_dir, "conan_profiles")
nla_recipes_dir = os.path.join(base_dir, "nla_recipes")

exclude_pkg_profiles = ["depot_tools", "crashpad"]
excluded_package_recipes = ["nla_pkg_helper"]

exec_common_cmd(["conan", "create"], "Create", "created", args.recipe_name, nla_recipes_dir,
                excluded_package_recipes, pkg_version=args.version, profile_name=args.profile_name,
                recipe_profile_exclusion_list=exclude_pkg_profiles,
                profiles_dir_path=profiles_dir, use_recipe_path=True)
