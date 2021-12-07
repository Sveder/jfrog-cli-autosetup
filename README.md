# Autosetup Repository Command Line Plugin 

## About this plugin
This plugin automatically sets up your local machine's package manager to 
work with your chosen remote artifactory repository.
For example, if you have a remote Artifactory repository
of type Pypi (Python package repo) this plugin will configure `pip` to be able to
work with it. 

## Installation with JFrog CLI
Installing the latest version:

`$ jfrog plugin install autosetup`

Installing a specific version:

`$ jfrog plugin install autosetup`

Uninstalling a plugin

`$ jfrog plugin uninstall autosteup`

Caveats for running python plugins:
1. The commands/handlers directory needs to be added to python path, most easily done with 
.pth file: https://docs.python.org/2/library/site.html
   
2. The commands/autosetup.py file (and directory) must be copied to the directory from which
you plan to use jfrog from.
   

## Usage
### Commands
* autosetup
    - Arguments:
        - repo - The name of the Artifactory repo you want to configure.
    - Example:
  ```
  $ jfrog autosetup <repo_name>
  Executing setup step...
  Local machine set up to work with <repo_name>
  ```
* teardown
    - Arguments:
        - repo - The name of the Artifactory repo you want to remove configuration.
    - Example:
  ```
  $ jfrog teardown <repo_name>
  Executing teardown step...
  Local machine no longer set up to work with <repo_name>
  ```


## Additional info
Currently, supported repository types:
* docker
* Pypi
* npm
* yum/rpm
* gems
* debian
* nuget
* conan


## Release Notes
The release notes are available [here](RELEASE.md).
