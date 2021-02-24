import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="Creates packages from NLA conan recipes")

parser.add_argument("recipe_name", help='The name of the recipe. Use "*" for all recipes.')
parser.add_argument("profile_name", help="The name of the conan profile to use.",
                    choices=["mac_os_arm64_profile", "mac_os_x86_64_profile", "windows_x86_64_mingw_msys2_profile"])
parser.add_argument("-vn", "--version", help="Package version to use if package allows for alternative versions.")

args = parser.parse_args()

common_cmd_dir = os.getcwd()
base_dir = os.path.dirname(common_cmd_dir)

nla_recipes_dir = os.path.join(base_dir, "nla_recipes")

exclude_pkg_profiles = ["depot_tools", "crashpad"]


def remove_profile_cmd_options_for_pkgs(recipe_name, cmd_opts_list):
    if cmd_opts_list and recipe_name and recipe_name in exclude_pkg_profiles:
        print(f"Package {recipe_name} will be created without profile option.")

        cmd_opts_list.pop()
        cmd_opts_list.pop()


if args.recipe_name == "*":
    successfully_created_pkgs = []
    failed_created_pkgs = []

    for root, dirs, files in os.walk(nla_recipes_dir):
        for recipe_dir in dirs:
            if recipe_dir == "nla_pkg_helper":
                continue

            print(f"Creating package: {recipe_dir}")

            cmd_opts = ["conan", "create", os.path.join(root, recipe_dir), "--profile",
                        os.path.join(base_dir, "conan_profiles", args.profile_name)]

            remove_profile_cmd_options_for_pkgs(recipe_dir, cmd_opts)

            completed_process = subprocess.run([cmd_opt for cmd_opt in cmd_opts], text=True, stderr=subprocess.STDOUT)

            if completed_process.returncode != 0:
                failed_created_pkgs.append(recipe_dir)
                print("Failed to create package: %s! Please check error details." % recipe_dir)
                continue

            successfully_created_pkgs.append(recipe_dir)
            print(f"Successfully created package: {recipe_dir}")

            print(f"{len(successfully_created_pkgs)} packages were successfully created:")
            for ok_pkg in successfully_created_pkgs:
                print(f"** Success ** - {ok_pkg}")

            print(f"{len(failed_created_pkgs)} failed package creations:")
            for bad_pkg in failed_created_pkgs:
                print(f"Failed - {bad_pkg}")
else:
    if args.recipe_name == "nla_pkg_helper":
        print("Package %s is a special package that cannot be created!" % "nla_pkg_helper")

    else:
        print(f"Creating package: {args.recipe_name}")

        cmd_opts = ["conan", "create", os.path.join(nla_recipes_dir, args.recipe_name),
                    f"{args.recipe_name}/{args.version}@" if args.version else "", "--profile",
                    os.path.join(base_dir, "conan_profiles", args.profile_name)]

        remove_profile_cmd_options_for_pkgs(args.recipe_name, cmd_opts)

        completed_process = subprocess.run([cmd_opt for cmd_opt in cmd_opts], text=True, stderr=subprocess.STDOUT)

        completed_process.check_returncode()

        print(f"Successfully created package: {args.recipe_name}")
