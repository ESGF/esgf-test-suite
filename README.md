esgf-test-suite
===============

Python (and bash) nosetests scripts for ESGF integration tests and validation

## Purpose and limits of this tool:

ESGF Test Suite is a full python application.

It is designed to perform integration tests on ESGF nodes.
The tests are organized as a acyclic graph and they can be refered to with a set of attributes.
In the given test\_plan.pdf, the leaf are the tests and the non terminal nodes are the attributes.
The underlined tests are implemented.

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

* Geckodriver installation (driver for Firefox):

Just download the latest version of the binary [here](https://github.com/mozilla/geckodriver/releases)
 (according to your OS) and add the path of the binary into the `PATH` environment variable.

    export PATH=/path/to/geckodriver:$PATH

* Python packages installation. Command for pip:

```
pip install nose splinter pyopenssl MyProxyClient requests nose-testconfig
```

### MacOSX

Tested with MacOSX Sierra and Miniconda for Python 2.7

* Geckodriver installation (driver for Firefox):

Just download the latest version of the binary [here](https://github.com/mozilla/geckodriver/releases) (according to your OS) and add the path of the binary into the `PATH` environment variable.

    export PATH=/path/to/geckodriver:$PATH

* Globus-url-copy installation

Globus-url-copy is part of the Globus Toolkit. You can install Globus Toolkit via: The offical Globus Toolkit package ([here](http://toolkit.globus.org/toolkit/downloads/latest-stable/)) or Homebrew:

      brew install globus-toolkit

* Python packages installation. Command for pip:

```
pip install nose splinter pyopenssl MyProxyClient requests nose-testconfig
```

## Configuration:

     vi [installation_dir]/esgf-test-suite/esgf-test-suite/default.ini   

Modify the nodes section and **save as with a different name** (like my\_config.ini). If several nodes are specified, they all should be in the same federation. Account section do not need to be modified.

## Usage:

The following examples except that you run the command in the `[installation_dir]/esgf-test-suite/esgf-test-suite/` directory
(yes twice, it is not a mistake) and the configuration file is named `my_config.ini`.

* Run all the tests:
```
nosetests -v --nocapture --nologcapture --tc-file my_config.ini 
```
Note: you can set the configuration file to be automatically loaded with the evironement variable `NOSE_TESTCONFIG_AUTOLOAD_INI`:

```
export NOSE_TESTCONFIG_AUTOLOAD_INI=/path/to/my_config.ini
nosetests -v --nocapture --nologcapture
```

* Run a set of tests according to the given nose attribute (for more information visit this [page](http://nose.readthedocs.io/en/latest/plugins/attrib.html))

This command line execute only the basic tests:
```
nosetests -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic'
```
**Note: attributes and tests relations are described in plan\_test.pdf .**

* Run a subset of tests according to the given nose attributes

This command line execute only the basic tests for the index node configured in `my_config.ini` (basic *AND* index attributes):
```
nosetests -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic,index'
```
Note: You may provide as many attributes as you want (logical operator will be *and*).

* Run sets of tests according to the given attributes

This example runs the union of the set of tests for the idp node and the set of tests for the index node (idp *OR* index):
```
nosetests -v --nocapture --nologcapture --tc-file my_config.ini -a 'idp' -a 'index'
```
Note: You may provide as many '-a' expressions as you want (logical operator will be *or*).

* Run the tests located in a particular directory.

This example runs the tests located in test/test\_node\_components/test\_index (the tests for index node).
```
nosetests -v --nocapture --nologcapture --tc-file my_config.ini utils ./test/test_node_components/test_index
```
Note: the `utils` directory is mandatory (esgf-test-suite python libraries).

* Run tests, overring configuration

This example run the basic tests for index node, overring the index node value from the default configuration: it tests the index node of LLNL:
```
nosetests -v --nocapture --nologcapture --tc-file default.ini -a 'basic,index' --tc='nodes.index_node:esgf-node.llnl.gov'
```
Note: the `nodes.index_node` corresponds to the section `nodes` and the key `index_node` in the configuration file.

* Run tests without providing any configuration file:

This example runs the basic tests for the index node of LLNL:
```
nosetests -v --nocapture --nologcapture -a 'basic,index' --tc='nodes.index_node:esgf-node.llnl.gov'
```
More informations about the command line options concerning the configuration [here](https://pypi.python.org/pypi/nose-testconfig).

## Remarks:

* This test suite needs to run and display an instance of Firefox. So if you run this test suite remotely, don't forget to enable X-Forwarding (ssh -Y or -X).
* This test suite can run with another browser than Firefox, provided a browser driver that will replace Geckodriver and modify your configuration file.
* Git ignores the geckodriver.log and my\_config.ini files.

DISCLAIMER - the scripts in this repo are provided as is - use at your own risk - they have been tested only on a single system and may require modification to work correctly on other systems.
