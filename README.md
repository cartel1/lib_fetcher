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