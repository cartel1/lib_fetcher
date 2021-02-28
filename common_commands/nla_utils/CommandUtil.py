import os
import subprocess
import traceback

from conans import tools


def _get_package_version(package_recipe_path, pkg_version):
    version = pkg_version or tools.load(os.path.join(package_recipe_path, "version.txt"))

    return version


def _print_pkg_processing_report(package_list, processing_ok, process_label_suffix):
    if package_list:
        print("%d %s package %s" % (
            len(package_list), ("successful" if processing_ok else "failed"), process_label_suffix))

        for pkg in package_list:
            print(f"{'** Success **' if processing_ok else '-- Failed --'} <-> {pkg}")


def exec_common_cmd(cmd_opts_list, cmd_title_label, cmd_suffix_label, pkg_name, nla_recipes_dir,
                    excluded_recipes_list, remote=None, pkg_version=None, profile_name=None,
                    recipe_profile_exclusion_list=None, profiles_dir_path=None, use_recipe_path=False):
    print(f"{cmd_title_label} package: {pkg_name}")

    successful_ops = []
    failed_ops = []
    pkg_process_exclusion_msg = "Processing of package %s is excluded!"

    for root, dirs, files in os.walk(nla_recipes_dir):
        for recipe_dir in dirs:
            if excluded_recipes_list and recipe_dir in excluded_recipes_list:
                print(pkg_process_exclusion_msg % pkg_name)
                continue

            if excluded_recipes_list and pkg_name and pkg_name in excluded_recipes_list:
                print(pkg_process_exclusion_msg % pkg_name)
                break

            cmd_opts = [cmd_opt for cmd_opt in cmd_opts_list]
            print("Input command template:")
            print(cmd_opts)

            if profile_name and profiles_dir_path:
                if recipe_profile_exclusion_list and (
                        pkg_name not in recipe_profile_exclusion_list or recipe_dir not in recipe_profile_exclusion_list):
                    cmd_opts.append("--profile")
                    cmd_opts.append(os.path.join(profiles_dir_path, profile_name))

            if use_recipe_path:
                cmd_opts.append(os.path.join(root, (recipe_dir if pkg_name == "*" else pkg_name)))

            the_pkg = (pkg_name if pkg_name != "*" else recipe_dir)
            the_version = (pkg_version or "") if pkg_name != "*" else None

            cmd_opts.append("%s/%s@" % (the_pkg, _get_package_version(os.path.join(root, the_pkg), the_version)))

            if remote:
                cmd_opts.append("-r")
                cmd_opts.append(remote)
            print("Command to be executed is:")
            print(cmd_opts)
            completed_process = subprocess.run([cmd_opt for cmd_opt in cmd_opts], text=True,
                                               stderr=subprocess.STDOUT)

            try:
                completed_process.check_returncode()
            except Exception as e:
                failed_ops.append(recipe_dir if pkg_name == "*" else pkg_name)
                print("Failed to process package: %s! Please check error details below: %s" % (
                    recipe_dir if pkg_name == "*" else pkg_name, e))
                traceback.print_exc()

                if pkg_name == "*":
                    continue
                else:
                    break

            successful_ops.append(recipe_dir if pkg_name == "*" else pkg_name)
            print("Successfully processed package: %s" % recipe_dir if pkg_name == "*" else pkg_name)

            if pkg_name != "*":
                break
        if pkg_name != "*":
            break

    _print_pkg_processing_report(successful_ops, True, cmd_suffix_label)
    _print_pkg_processing_report(failed_ops, False, cmd_suffix_label)
