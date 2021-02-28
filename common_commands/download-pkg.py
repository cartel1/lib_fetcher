import argparse
import os

from nla_utils.CommandUtil import exec_common_cmd

parser = argparse.ArgumentParser(
    description="Download packages from a specified remote Conan Package Manager Repository.")

parser.add_argument("package",
                    help='The name of the package to download. Use "*" (including quotes) to download all packages.')
parser.add_argument("-vn", "--version", help="Package version to download.")
parser.add_argument("remote", help="Name of Conan remote")

args = parser.parse_args()

common_cmd_dir = os.getcwd()
base_dir = os.path.dirname(common_cmd_dir)
nla_recipes_dir = os.path.join(base_dir, "nla_recipes")

excluded_package_recipes = ["nla_pkg_helper"]

exec_common_cmd(["conan", "download"], "Download", "downloads", args.package, nla_recipes_dir,
                excluded_package_recipes, remote=args.remote, pkg_version=args.version)
