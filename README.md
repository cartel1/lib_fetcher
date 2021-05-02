# Introduction

lib_fetcher is a build tool for the source code of C and C++ libraries and applications.  

lib_fetcher relies heavily on the Conan Python module for the vast majority of its functionality.

To build the source code of your C and C++ projects for various operating system platforms and computer
architectures, you will create Conan recipes in particularly named directories which are then required 
to be stored in the lib_fetcher "recipes" directory which will cause lib_fetcher to detect and execute the Conan 
recipe file for the C and C++ source code files you're interested in building.

Source code files can be automatically downloaded from a web-server and unzipped or checked out of a 
specified Git repository and then automatically built according to configuration and build logic outlined
in the Conan file created and associated with the build.

The following sections will outline the lib_fetcher setup and execution requirements to be able to
access the source code of C and C++ libraries and applications located in remote repositories and to execute
the build process on Windows and MacOS computers.

## Setup and Build Execution Instructions for Windows 10 x64 Computers

### Software Requirements

- **Microsoft Visual Studio 2019**

    Download and install Microsoft Visual Studio and the Microsoft C/C++ tools based on instructions found 
  [here](https://docs.microsoft.com/en-us/cpp/build/vscpp-step-0-installation).  You can install the community edition, 
  and the primary workload configuration selection should be "Desktop development with C++" workload.


- **Python 3**

  Download the latest Python 3 installer for Windows 10 and install it.  A Python 3 installer for 
  Windows 10 x64 can be sourced [here](https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe).  
  Make sure to select the option to also install PIP 3 on the installation dialog window.
  
  Use the pacman package manager tool to install the latest version of Python 3 for MSYS2 via  
  

- **PIP 3**
  
  Verify that pip3 was installed by the Python installer for Windows, by typing:

  >pip3 --version
  
   at a windows command prompt. If pip3 is installed, you should the see the version details displayed
   in command terminal window.  If it has been determined that pip3 was not installed, just re-run the
   Python 3 Windows installer and make sure you opt to select to install pip3 on the installation dialog
   window.
  
  
- **Conan**

    Install the Conan build module by running the following command at a windows command prompt:

  > pip3 install conan
  
  After Conan has been installed, locate the following file in your user home directory and open it in a text editor:

  > .conan/settings.yml
  
  Once the settings.yml file is open, do the following:

  1. Navigate to the following section - ***compiler: gcc: version:***
  
  2. At the end of the list of versions, type: "10.2" after a comma.
  
  3. Save the settings.yml file and exit.

- **MSYS2**

  Download and install MSYS2 based on instructions found [here](https://www.msys2.org).  After MSYS2 has been installed, 
  open an x64 MSYS2 terminal window and use the pacman package manager tool to ensure that the latest version of Python 3 
  (greater than 3.8+), pip 3, and Conan as mentioned above.
  

- **MINGW-W64**

  Use the MSYS2 pacman package manager tool to install the mingw-w64 tool chain using the instructions found 
  [here](https://www.msys2.org).
  
### Build Instructions

The following instructions outline how to build libraries and executables on Windows 10 x64 by running various lib_fecther
command-line scripts and options:

 1. Open a developer command prompt window and run the vcvars64.bat file to setup an x64 build environment. Please see
      more details [here](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-160)


 2. Once the x64 build environment is setup, leave the developer command prompt window open and run the following 
    command to open an x64 msys2 terminal window:
  
    > C:\<msys2_home_directory>\msys2_shell.cmd -mingw64 
    
    where <msys2_home_directory> represents the home directory of your MSYS2 installation - e.g. msys64. The msys2 
    terminal window should now be open along with the previously opened developer tools command prompt.
   
 
 3. In the msys2 terminal, check to ensure that python 3, pip 3, perl and the mingw-w64 toolchain is installed.  If 
    anything is missing, use the pacman package manager to install it.
    
    
 4. At this point, you will now be able to build the libs using mingw-w64 and msvc toolchains.


 5.  While still in the open msys2 terminal, install conan via pip 3 (if not installed) and clone the lib_fetcher git
     repository.
     
     
 6. After cloning the lib_fetcher repository, cd to the lib_fetcher directory and then run the lib_fetcher init-sys.py 
    script. E.g:
    
    > python3 init-sys.py 
     
 
 7. If the init-sys.py script runs ok in msys2, run the create-pkg.py script with the "*" argument to build all libs 
    using the profile option that's appropriate to the OS platform and toolchain being used to run the build. For the
    latter, you will typically use profile ***windows_x86_64_msvc_mingw_msys2_profile*** for windows builds using
    msys2 and mingw-w64 or profile ***windows_x86_64_profile*** for builds using the developer command 
    prompt window and the msvc compiler. E.g:
    
    > python3 create-pkg.py "*" windows_x86_64_msvc_mingw_msys2_profile
    
    or

    > python3 create-pkg.py "*" windows_x86_64_profile
    
    ***Please note that some builds for recipes will fail. These failed recipe builds must be identified and built in the 
   developer tool command prompt window.***


  8.  For the builds that failed in msys2, note them down and build them separately in the currently open developer tools 
      command prompt window by doing the following:
      
      (a) Ensure that python 3, pip 3, and conan are installed.

      (b) Clone the lib_fetcher git repository.

      (c) Run the init-sys.py script as explained previously.

      (d) Run the create-pkg.py script (explained previously) to build the previously failed msys2 mingw-w64 recipe 
          builds.
      
      
    Important! The recipes for Crashpad. Poco, and Protobuf should be built with the MSVC compiler in the developer tools 
    prompt window with x64 build environment.
    
    Use windows_x86_64_profile to build libs in the developer tools windows with x64 build environment context.
    
    Use windows_x86_64_msvc_mingw_msys2_profile to build libs in the msys2 terminal.
      
## Setup and Build Execution Instructions for MacOS 10+ x86_64 and arm64 Computers

### Software Requirements

- **Apple Xcode and Xcode Developer Tools**

    Install Apple Xcode on your Mac. You can install Xcode using the Apple store application on your Mac. Once you’ve 
    installed Xcode, open a terminal window and type:
  
    > sudo xcode-select --install

    This will install the required command line developer tools. Then accept Xcode license by executing:

    > sudo xcodebuild -license

- **Python 3**

  Download and install the latest Python 3 version ( 3.8+) using your preferred package management tool,
  example homebrew (recommended). E.g:
  
  > brew install python3
  

- **PIP 3**
  
  If you had installed Python 3 using homebrew, PIP 3 would have been installed automatically. Verify that PIP 3 was 
  installed by the Python 3 installation by typing the following at a terminal prompt window:

  >pip3 --version
  
   If PIP 3 is installed, you should the see the version details displayed in the command terminal window.  If it has been 
   determined that pip3 was not installed, re-run the Python 3 installer and make sure you opt to select to install 
   PIP 3 or uninstall Python 3 and install it again using homebrew.
  
  
- **Conan**

    Install the Conan build module by running the following command at a terminal prompt window: 

  > pip3 install conan
  
  After Conan has been installed, locate the following file in your user home directory and open it in a text editor:

  > .conan/settings.yml
  
   Once the settings.yml file is open, do the following:

  1. Navigate to path - arch:
  
  2. In the list of archs, insert value "arm64" at the end of all the arm* subset of values. The arm64 value should be 
     inserted in the list without quotes just like the other values.
     
  3. Navigate to the following section - ***compiler: gcc: version:***
  
  4. At the end of the list of versions, type: "10.2" after a comma.
  
  5. Save the settings.yml file and exit.  
  

- **Unix Autotools (Automake, Autoconf, Libtool) and CMake**

  Install automake, autoconf, libtool and cmake with your preferred package manager, e.g. homebrew (recommended). E.g:

  > brew install autoconf automake libtool cmake
  

### Build Instructions

The following instructions outline how to build libraries and executables on MacOS 10+ x64 and arm64 computers by 
running various lib_fecther command-line scripts and options:

 1.  Open a terminal window and clone the lib_fetcher git repository.
     
     
 6. After cloning the lib_fetcher repository, cd (change directory) to the lib_fetcher directory and then cd to the 
    common_commands directory. Once in the common_commands directory, run the lib_fetcher init-sys.py 
    script with a profile specific to a MacOS x86_64 or MacOS arm64 machine. E.g:
    
    > python3 init-sys.py <mac_os_arm64_profile or mac_os_x86_64_profile>
     
 
 7. If the init-sys.py script runs ok, run the create-pkg.py script with the "*" argument to build all libs 
    using the profile option that's appropriate to the OS platform and architecture being used to run the build. For the
    latter, you will typically use profile ***mac_os_arm64_profile*** for MacOS arm64 builds and profile 
    ***mac_os_x86_64_profile*** for MacOS x86_64 builds. E.g:
    
    > python3 create-pkg.py "*" mac_os_arm64_profile
    
    or

    > python3 create-pkg.py "*" mac_os_x86_64_profile
    
    ***Please note that some builds for recipes will fail. These failed recipe builds must be identified and are usually
    associated with recipes that can only be built on Windows OS machines.***
    
## Setup Instructions for a Conan Package Manager Repository (Optional) 
A Conan package manager repository is used to centrally store the build artefacts of the fetched source code of libraries and
executables. Such build artefacts include static and shared libs, binary executables, header files and Conan recipes and
packages.

A Conan package manager repository will provide proper segregated storage for packages generated from Conan recipes
that are associated with multiple OS platforms and architectures.

Follow the instructions [here](https://docs.conan.io/en/latest/uploading_packages/running_your_server.html?highlight=gunicorn#server-configuration) which outlines the steps needed to setup a Conan package manager repository
and server such as Gunicorn (recommended).

### Setup Package Manager Repository Remotes and Authentication

After a Conan package manager repository and server has been established and configured with the necessary allowed user
credential as explained [here](https://docs.conan.io/en/latest/uploading_packages/running_your_server.html?highlight=gunicorn#server-configuration),
you will need to configure your build machine to be able to access the repository manager and provide the necessary credentials
to be able to push or download generated packages.


Open a command-line terminal window and run the following command to setup a reference to the package manager repository: 

> conan remote add <arbitrary_name_of_remote> http://<ip_address_of_repository_manager>:<port> --insert=0
 
where: 

< arbitrary_name_of_remote > - is a name you provide for the Conan remote reference you'd like to create (without spaces)

< ip_address_of_repository_manager > - is the ip address or host name of the computer running the package manager repository
and server.


< port > - is the port number configured and exposed by the configuration of the package manager repository and server.

Example:

> conan remote add nla-conan-repo http://162.174.15.1:9300 --insert=0


Once you have an account/access credentials configured on the repository manager server, run the following command to add 
your account credentials to the Conan client:

> conan user < your-user-account > -r < name_of_remote > -p < your user account password >

where:

< your-user-account > - is the user account configured on the repository manager server.

< name_of_remote > - is the name of the previosuly created Conan remote reference to the URL of the repository manager.

< your user account password > - is the user account password configured on the repository manager server

Example:

> conan user user1 -r nla-conan-repo -p user1-password

At this point, you should  now be able to upload and download packages to and from the repository manager.

## Command-line Scripts User Guide

The following sections will describe the command-line scripts needed manage the life cycle of the builds.

***Important! Before running any command-line script, open a command terminal window and cd to the common_commands 
subdirectory in the lib_fetcher directory. All command-line scripts must be run from the common_commands subdirectory.***

### System Initialization
If you plan on building multiple recipes at once by running the commanad ```python3 create-pkg.py "*"```, you must 
first do an initialisation step by running the following command in a command-line terminal window:

For Mac OS:

> python3 init-sys.py < mac_os_arm64_profile or mac_os_x86_64_profile > 

For Windows 10:

> python3 init-sys.py < windows_x86_64_profile or windows_x86_64_msvc_mingw_msys2_profile >  

### Building Binary Libraries and Executables from Conan Recipes
After running init-sys.py, you can now run the following commands to run all recipe builds for a specific recipe build.

***Important! All recipes are listed in the nla-recipes folder. A recipe name is the folder name of the recipe.***

For Mac OS:

> python3 create-pkg.py "*" < mac_os_arm64_profile or mac_os_x86_64_profile >

> python3 create-pkg.py < recipe_name > < mac_os_arm64_profile or mac_os_x86_64_profile > 

Example:

> python3 create-pkg.py "*" mac_os_x86_64_profile

> python3 create-pkg.py ffmpeg mac_os_arm64_profile

For Windows:

> python3 create-pkg.py "*" < windows_x86_64_profile or windows_x86_64_msvc_mingw_msys2_profile > 

> python3 create-pkg.py < recipe_name > < windows_x86_64_profile or windows_x86_64_msvc_mingw_msys2_profile > 

Example:

> python3 create-pkg.py "*" windows_x86_64_msvc_mingw_msys2_profile

> python3 create-pkg.py ffmpeg windows_x86_64_msvc_mingw_msys2_profile

### Removing Conan Packages
All created packages are stored in the following location:

> < user_home_directory >/.conan/data

where:

< user_home_directory > - is the home directory of the user running the lib_fetcher scripts.

Example:

> ~/.conan/data

All subdirectories located in the ***~/.conan/data*** directory are the packages that were built from their respective
recipes.  You can delete specific package subdirectories or all subdirectories as required using standard operating 
system terminal commands or via normal highlighting and deleting of all or specific directories using the OS specific file
explorer application.

Example:

> rm -rf ffmpeg


### Uploading Packages
After creating the packages on your build machine using the create-pkg.py script, you can then push/upload them to the 
package manager server repo by running the following script to upload all packages or a specific package:

> python3 upload-pkg.py "*" < name_of_package_repo_remote >

or

> python3 upload-pkg.py < recipe_name > < name_of_package_repo_remote >

Example:

> python3 upload-pkg.py "*" nla-conan-repo

or

> python3 upload-pkg.py ffmpeg nla-conan-repo

### Downloading Packages

To download all packages or a specific package from the package manager repository, run the following scripts:

>  python3 download-pkg.py "*" < name_of_package_repo_remote >

or 

> python3 download-pkg.py < recipe_name > < name_of_package_repo_remote >

Example:

> python3 download-pkg.py "*" nla-conan-repo

or

> python3 download-pkg.py ffmpeg nla-conan-repo

## Locating Built Artefacts for Windows and MacOS Builds

After running the create-pkg.py script to create packages from recipes as described in previous sections, you can locate
generated binaries for static and dynamic libraries, executables and header files in the respective OS specific package 
deployment subdirectory of the .conan directory which is located in the user's home directory.


On MacOS x86_64 machines, the package deployment subdirectory is located in the following path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/macosx_x86_64


On MacOS arm64 machines, the package deployment subdirectory is located in the following path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/macosx_arm64


On MacOS x86_64 machines, the package deployment subdirectory for generated universal binaries is located in the following 
path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/macosx_x86_64/macosx_universal


On MacOS arm64 machines, the package deployment subdirectory for generated universal binaries is located in the following 
path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/macosx_arm64/macosx_universal


On Windows x86_64 machines, the package deployment subdirectory is located in the following path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/win10_x86_64

Example:

> ~/.conan/data/poco/1.10.1/_/_/package/259c493fd8eb79c7bfe0d64db3c2b75acfbf8064/macosx_x86_64

## A Note on MacOS Universal Binaries
If the local .conan/data package cache directory of the current build machine contains packages for recipes associated with 
binaries that were built on a machine with an architecture that is different from the current build machine, universal binaries will be automatically created whenever the create-pkg.py script is run
for recipes with the same name on the current build machine will be automatically generated whenever the
create-pkg.py script is executed.

On MacOS x86_64 build machines, the package deployment subdirectory for generated universal binaries is located in the following 
path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/macosx_x86_64/macosx_universal


On MacOS arm64 build machines, the package deployment subdirectory for generated universal binaries is located in the following 
path structure:

> <user_home_directory>/.conan/data/<recipe_package_name>/<recipe_package_version>/_/_/package/<recipe_package_id>>/macosx_arm64/macosx_universal


Example:

> ~/.conan/data/poco/1.10.1/_/_/package/259c493fd8eb79c7bfe0d64db3c2b75acfbf8064/macosx_x86_64/macosx_universal


##A Note on Building Shared vs Static Libraries with the create-pkg.py Script

When building specific recipes with the create-pkg.py script, you can optionally specify the --shared or -sh flag which takes a value of True or False
which will cause the create-pkg.py script to try and create Conan packages with shared library artefacts, or static library artefacts respectively.

Please note that the optional shared flag is not guaranteed work for all recipes as the source code and build configuration files for third party
libraries and applications downloaded by lib_fetcher may have default internal build settings which cannot be altered.

An Example use of the shared flag is shown below:

> python3 create-pkg.py poco mac_os_x86_64_profile --shared=True


## A Note on Getting Help When Using a lib_fetcher Command-line Script

If you want to run a lib_fetcher script, and you forget the details about the required command line arguments and flags, you can simply specify
the name of the script along with the --help or -h flag, and the help details for the command-line script will be displayed onscreen.

Example:

> python3 create-pkg.py --help