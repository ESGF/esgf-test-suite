esgf-test-suite
===============

Python (and bash) nosetests scripts for ESGF integration test and validation

## UPDATE 10/20/2017

* Adding LLNL scripts to deploy a full node test on a remote VM (controled using vmware vmrun on the local server host OS).  


## Purpose and limits of this tool:

ESGF Test Suite is a full python application. It is designed to perform integration tests on ESGF nodes. At this point of time, the scope is to test a single data node and its three peer services (idp services, index services and compute services).

ESGF Test Suite offers to run high level tests from a desktop so the tested node can be validated from the end user perspective.

Current developments will also let admins to test and validate the stack by running tests on the node itself.

## Requirements:

- Shell environment  
- Python 2.6 or higher
- Firefox
- Globus-url-copy (Globus Toolkit)
- Nose
- Splinter
- Pyopenssl (OpenSSL)
- MyProxyClient
- Geckodriver
- LibXML
- LibXSLT

## Installation

### Linux

* OS packages installation.

Command for Red Hat / CentOS / Scientifix Linux:
     
     yum install python-devel openssl-devel libxml2-devel libxslt-devel globus-gass-copy-progs firefox

Command for Debian like Systems:
     
     apt-get install python2.7-dev libssl-dev libxml2-dev libxslt-dev globus-gass-copy-progs firefox

* Geckodriver installation:

Just download the latest version of the binary [here](https://github.com/mozilla/geckodriver/releases)
 (according to your OS) and add the path of the binary into the PATH environment variable.

    export PATH=/path/to/geckodriver:$PATH

* Python packages installation. Command for pip:

```
pip install nose splinter pyopenssl MyProxyClient requests nose-testconfig
```

### MacOSX

Tested with MacOSX Sierra and Miniconda for Python 2.7

* Geckodriver installation:

Just download the latest version of the binary [here](https://github.com/mozilla/geckodriver/releases) (according to your OS) and add the path of the binary into the PATH environment variable.

    export PATH=/path/to/geckodriver:$PATH

* Globus-url-copy installation

Globus-url-copy is part of the Globus Toolkit. You can install Globus Toolkit via: The offical Globus Toolkit package ([here](http://toolkit.globus.org/toolkit/downloads/latest-stable/)) or Homebrew:

      brew install globus-toolkit

* Python packages installation. Command for pip:

```
pip install nose splinter pyopenssl MyProxyClient requests nose-testconfig
```

## Configuration:

     vi [installation_dir]/esgf-test-suite/configuration.ini   

Modify the nodes section. If several nodes are specified, they all should be in the same federation. Account section do not need to be modified.

To make git ignore your configuration:

```
git update-index --assume-unchanged [installation_dir]/esgf-test-suite/configuration.ini
```

To undone:

```
git update-index --no-assume-unchanged [installation_dir]/esgf-test-suite/configuration.ini
```

## Usage:

* Run all the tests:
     
     [installation_dir]/esgf-test-suite/runtests.sh

* Run a particular test:

     nosetests [installation_dir]/utils [installation_dir]/esgf-test-suite/test_0_webfrontends.py -v --exe --nocapture --nologcapture


## Remarks:

* This test suite needs to run and display an instance of firefox. So if you run this test suite remotely, don't forget to enable X-Forwarding (ssh -Y or -X).

DISCLAIMER - the scripts in this repo are provided as is - use at your own risk - they have been tested only on a single system and may require modification to work correctly on other systems.
