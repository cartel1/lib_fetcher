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

- **Python 3**

  Download the latest Python 3 installer for Windows 10 and install it.  A Python 3 installer for 
  Windows 10 x64 can be sourced [here](https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe).  
  Make sure to select the option to also install PIP 3 on the installation dialog window.
  

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

   