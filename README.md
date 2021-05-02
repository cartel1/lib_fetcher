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

## Setup and Build Execution Requirements for Windows 10 x64 Computers

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
      
## Setup and Build Execution Requirements for MacOS 10+ x86_64 and arm64 Computers

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
  

- **Unix Autotools (Automake, Autoconf, Libtool)**

  Install automake, autoconf, and libtool with your preferred package manager, e.g. homebrew (recommended). E.g:

  > brew install autoconf automake libtool
  

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


 