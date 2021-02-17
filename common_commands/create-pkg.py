import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="Creates packages from NLA conan recipes")

parser.add_argument("recipe_name", help="The name of the recipe. Use * for all recipes.")
parser.add_argument("profile_name", help="The name of the conan profile to use.")
parser.add_argument("-vn", "--version", help="Package version to use if package allows for alternative versions.")

args = parser.parse_args()

common_cmd_dir = os.getcwd()
base_dir = os.path.dirname(common_cmd_dir)

nla_recipes_dir = os.path.join(base_dir, "nla_recipes")

if args.recipe_name == "*":
    for root, dirs, files in os.walk(nla_recipes_dir):
        for recipe_dir in dirs:
            if recipe_dir == "nla_pkg_helper":
                continue

            print(f"Creating package: {recipe_dir}")

            completed_process = subprocess.run(
                ["conan", "create", os.path.join(root, recipe_dir), "--profile",
                 os.path.join(base_dir, "conan_profiles", args.profile_name)], text=True, stderr=subprocess.STDOUT)

            if completed_process.returncode != 0:
                print("Failed to create package: %s! Please check error details." % recipe_dir)
                continue

            print(f"Successfully created package: {recipe_dir}")
else:
    if args.recipe_name == "nla_pkg_helper":
        print("Package %s is a special package that cannot be created!" % "nla_pkg_helper")

    else:
        print(f"Creating package: {args.recipe_name}")
        completed_process = subprocess.run(
            ["conan", "create", os.path.join(nla_recipes_dir, args.recipe_name),
             f"{args.recipe_name}/{args.version}@" if args.version else "", "--profile",
             os.path.join(base_dir, "conan_profiles", args.profile_name)], text=True, stderr=subprocess.STDOUT)

        completed_process.check_returncode()

        print(f"Successfully created package: {args.recipe_name}")
