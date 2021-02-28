import argparse
import os

from nla_utils.CommandUtil import exec_common_cmd

parser = argparse.ArgumentParser(
    description="Delete packages from the local Conan package cache.")

parser.add_argument("package",
                    help='The name of the package to delete. Use "*" (including quotes) to delete all packages.')
parser.add_argument("-vn", "--version", help="Package version to delete.")

args = parser.parse_args()

common_cmd_dir = os.getcwd()
base_dir = os.path.dirname(common_cmd_dir)
nla_recipes_dir = os.path.join(base_dir, "nla_recipes")

excluded_package_recipes = ["nla_pkg_helper"]

exec_common_cmd(["conan", "remove", "-f"], "Delete", "delete(s)", args.package, nla_recipes_dir,
                excluded_package_recipes, remote=None, pkg_version=args.version)
