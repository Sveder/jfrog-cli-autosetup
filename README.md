# Autosetup Repository Command Line Plugin 

## About this plugin
This plugin automatically sets up your local machine to work with your chosen remote
artifactory repositories. For example, if you have a remote Artifactory repository
of type Pypi (Python libraries repo) this plugin will configure `pip` to be able to
work with it. 

## Installation with JFrog CLI
Installing the latest version:

`$ jfrog plugin install autosetup`

Installing a specific version:

`$ jfrog plugin install autosetup`

Uninstalling a plugin

`$ jfrog plugin uninstall autosteup`

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

## Additional info
Currently supported repository types:
* docker
* Pypi


## Release Notes
The release notes are available [here](RELEASE.md).
