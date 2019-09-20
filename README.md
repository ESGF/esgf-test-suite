esgf-test-suite
===============

Python (and bash) nosetests scripts for ESGF integration tests and validation

## TLDR

Well, it is nearly impossible to run esgf-test-suite without reading entirely this man. Sorry.

### Recommanded tests for a classical ESGF installation

* Without SLCS
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a '!compute,!cog_create_user,!slcs' --with-id
```

* With SLCS
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a '!compute,!cog_create_user' --with-id
```

Don't forget to configure the superset to the value _classic_ in the configuration file.

### Recommanded tests for a ESGF docker deployement

```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic,!compute' -a 'slcs' --with-id
```
Don't forget to configure the superset to the value _docker_ in the configuration file (see section Configuration).

### Understanding the result of the tests

* `ok`: the service been tested is alright.
* `ERROR`: the test has crashed. Please report an issue on [github](https://github.com/ESGF/esgf-test-suite/issues)
* `FAIL`: the test has not crashed but the service, that has been tested, failed.

## Purpose and limits of this tool:

ESGF Test Suite is a full python application.

It is designed to perform integration tests on ESGF nodes.
The tests are organized as a acyclic graph and they can be refered to with a set of attributes.
In the ./esgf-test-suite/doc/test\_plan.pdf, the leaf are the tests and the non terminal nodes are the attributes.
The underlined tests are implemented.

ESGF Test Suite offers to run high level tests from a desktop so the tested node can be validated from the end user perspective.
Current developments will also let admins to test and validate the stack by running tests on the node itself.

## Requirements:

- Shell environment  
- Python 3.6 or 3.7 (but not 2.x ; 3.8 is untested)
- Firefox (tested version: 60.7.0esr) **!! esgf-test-suite/Gekodriver doesn't work with versions of Firefox less than 58 (like the esr channel) !!**
- Globus-url-copy (MacOSX/homebrew: Globus Toolkit 6.0.1506371041 ; Linux: globus-gass-copy-progs 10.4-1) 
- Nose (tested version: 1.3.7)
- Pyopenssl (OpenSSL ; tested version: 19.0.0)
- MyProxyClient (tested version: 2.1.0)
- Myproxy (tested version v6.2)
- Geckodriver (tested version: 0.24.0)
- Selenium (tested version 3.141.0)
- Requests (tested version 2.22.0)
- LibXML (tested version: 2.9.1-6)
- LibXSLT (tested version: 1.1.28-5)
- LXML (tested version: 4.3.4)
- Nose-testconfig (tested version: 0.10)
- Nose-htmloutput (tested version: 0.6.0)

## Installation

### Linux

Tested on CentOS 7.

* OS packages installation.

Command for Red Hat / CentOS / Scientifix Linux 7:
     
     yum install openssl-devel libxml2-devel libxslt-devel globus-gass-copy-progs firefox myproxy

* Geckodriver installation (driver for Firefox):

Just download the latest version of the binary [here](https://github.com/mozilla/geckodriver/releases)
 (according to your OS) and add the path of the binary into the `PATH` environment variable.

    export PATH=/path/to/geckodriver:$PATH

* Python packages installation. Command for pip:

```
pip install -U nose pyopenssl MyProxyClient selenium requests nose-testconfig nose-htmloutput lxml
```
* Clone this repository

Then cd to the directory `[parent_directory]/esgf-test-suite/esgf-test-suite/` (yes twice, it is not a mistake).

Note: the branch master is always at the last stable version.

```
git clone https://github.com/ESGF/esgf-test-suite.git
cd ./esgf-test-suite/esgf-test-suite
```

### MacOSX

Untested on MacOSX. Sorry, waiting for feedback...

* Geckodriver installation (driver for Firefox):

Just download the latest version of the binary [here](https://github.com/mozilla/geckodriver/releases) (according to your OS) and add the path of the binary into the `PATH` environment variable.

    export PATH=/path/to/geckodriver:$PATH
    
OR

Install Geckodriver via Homebrew:

     brew install geckodriver

* Globus-url-copy installation

Globus-url-copy is part of the Globus Toolkit. You can install Globus Toolkit via: The offical Globus Toolkit package ([here](http://toolkit.globus.org/toolkit/downloads/latest-stable/)) or Homebrew:

      brew install globus-toolkit

* Python packages installation. Command for pip:

```
pip install -U nose pyopenssl MyProxyClient selenium requests nose-testconfig nose-htmloutput lxml
```

* Clone this repository

Then cd to the directory `[parent_directory]/esgf-test-suite/esgf-test-suite/` (yes twice, it is not a mistake).

Note: the branch master is always at the last stable version.

```
git clone https://github.com/ESGF/esgf-test-suite.git
cd ./esgf-test-suite/esgf-test-suite
```

### Singularity

Tested with Singularity 2.5.2-dist on CentOS 7.

A Singularity image of container is also available. At the moment, it only packages the dependencies (python, pip packages, etc.) of the esgf-test-suite and not the test-suite itself.
This image is built from the offical docker image of the latest version of LTS Ubuntu (Singularity recipe is described [here](https://github.com/ESGF/esgf-test-suite/blob/master/esgf-test-suite/singularity/esgf-test-suite.def)).

* Linux

  * Install Singularity (procedure available [here](https://sylabs.io/guides/3.2/admin-guide/admin_quickstart.html#installation))
  
  * Download the image [here](http://distrib-coffee.ipsl.jussieu.fr/pub/esgf/dist/esgf-test-suite/esgf-test-suite_env.singularity.img) (sha1: 010d031bd258b21d149ad0a0920de71a90b8fc7a)
    The image that works with Python 2 is still available [here](http://distrib-coffee.ipsl.jussieu.fr/pub/esgf/dist/esgf-test-suite/esgf-test-suite_env.singularity.img.py2) (sha1: 869b98a087a24b08bfcf394ad7028fb3a606215c)

  * Clone this repository then cd to it: `git clone https://github.com/ESGF/esgf-test-suite.git ; cd ./esgf-test-suite/esgf-test-suite`

  * Turn on the esgf-test-suite environment image, once per session: `singularity shell esgf-test-suite_env.singularity.img`

* MacOSX

  * Create a Linux virtual machine (procedure available [here](http://singularity.lbl.gov/install-mac))
  * ssh into the virtual machine: `vagrant ssh`
  * Download the image [here](http://distrib-coffee.ipsl.jussieu.fr/pub/esgf/dist/esgf-test-suite/esgf-test-suite_env.singularity.img) (sha1: 010d031bd258b21d149ad0a0920de71a90b8fc7a)
    The image that works with Python 2 is still available [here](http://distrib-coffee.ipsl.jussieu.fr/pub/esgf/dist/esgf-test-suite/esgf-test-suite_env.singularity.img.py2) (sha1: 869b98a087a24b08bfcf394ad7028fb3a606215c)
  * Clone this repository then cd to it: `git clone https://github.com/ESGF/esgf-test-suite.git ; cd ./esgf-test-suite/esgf-test-suite`
  * Turn on the esgf-test-suite environment image, once per session: `singularity shell esgf-test-suite_env.singularity.img`

## Configuration:

Configuration file is meant to be modified according to your needs and
**save as with a different name** (like my\_config.ini).
Git ignores files with the following pattern my\_config\*.ini

     vi [installation_dir]/esgf-test-suite/esgf-test-suite/default.ini   

esgf-test-suite raises a ConfigurationException if the configuration file is
wrong or incomplete.
However, you don't have to fullfill the entire configuration file:
you just have to give the information needed for the tests that you want to execute.

* Section test

  - entry `type` allows you to select the superset of tests that corresponds to
    the type your ESGF stack installation. Choose the value `classic` to run the
    set of tests that aims a 'classical' installation of the ESGF stack. Choose the
    value `docker` to run the set of tests that aims a 'docker' installation of the ESGF stack
  - entry `web_page_timeout` configures the timeout (integer in seconds) when waiting for a web page (i.e. CoG login)
  - entry `download_timeout` configures the timeout (integer in seconds) when downloading files (i.e. download tests)

* Section nodes:

  - `idp_node`: the idp node
  - `data_node`: the data node
  - `index_node`: the index node
  - `compute_node`: the compute node
  - `gridftp_node`: the gridftp node

Specify the full qualified address of your nodes.
You may leave some entries empty, but ESGF-test-suite won't let you run the tests
that need the missing addresses.

* Section account
 
  - `firstname`: set the user's first name
  - `lastname`: set the user's last name
  - `email`: set the user's email address
  - `username`: set the login name of the account
  - `password`: set the password of the account
  - `institution`: set the user's institution
  - `city`: set the user's city
  - `country`: set the user's country

This section describes the user account to be used for the login and downloading
tests (cog, myproxy and http download tests).

Note: The creation of an account (test named: cog_create_user) through the CoG
interface is not possible until the captcha is disable.
Both user creation and user login tests rely on the section `account`.
You cannot create a user that already exists.

* Section browser

  - `soft`: specifies the browser to use. Firefox is only support for the moment.
  - `is_headless`: set the value to `false`, only if you want to display firefox
    when the tests are running (debugging). **esgf-test-suite/selenium/geckodriver requires that the window of Firefox keeps
    the focus while the tests are running. So don't switch to other windows when is_headless is set to True**

This section let you configure the browser used to test CoG and other services.

* Section cog

  - `admin_username`: set the admin's login name
  - `admin_password`: set the admin's password 

Testing CoG requires some information. This section provides the required
information.

* Section slcs

  - `admin_username`: set the admin's login name
  - `admin_password`: set the admin's password 

Testing SLCS requires some information. This section provides the required
information.  

* Section sys

  - `is_debug`: set to `true` to output debugg information and to stop closing
   the browser at the end of the execution.

This section configures the development options.

## Understanding the result of the tests

* `ok`: the service been tested is alright.
* `ERROR`: the test has crashed. Please report an issue on [github](https://github.com/ESGF/esgf-test-suite/issues)
* `FAIL`: the test has not crashed but the service, that has been tested, failed.

## Usage:

The following examples except that you run the command in the
`[installation_dir]/esgf-test-suite/esgf-test-suite/` directory
(yes twice, it is not a mistake) and the configuration file is named `my_config.ini`.
ESGF-test-suite is based on the nose attributes, for more information about them,
visit this [page](http://nose.readthedocs.io/en/latest/plugins/attrib.html)

* Nose options
  - `--with-html` generates a nice htlm report without the python traceback when tests fail (default report file name is 'nosetests.html').
  - `--with-id` generates the id of the tests so you can rerun next time tests of your choice calling nosetest with `--with-id #` where # is the id numbers (space is the separator).
  - `--failed` keeps nosetest to loop over the failed tests (like `--with-id` with the id of the failed tests).
  - `--rednose --force-color --hide-skips` this one colors the output of nosetests but I will have to install rednose: `pip install rednose`. Do not use this option when redirecting the output into a file.

The nosetest doc is available [here](http://nose.readthedocs.io/en/latest/testing.html)

* Run all the tests:
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini 
```
Note: you can set the configuration file path to be automatically loaded with the environment variable `NOSE_TESTCONFIG_AUTOLOAD_INI`:

```
export NOSE_TESTCONFIG_AUTOLOAD_INI=/path/to/my_config.ini
python3 esgf-test.py -v --nocapture --nologcapture
```

* Run a set of tests according to a nose attribute

This command line executes only the basic tests:
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic'
```
Note: see the section _test selection_ for more information about nose attributes.

* Run an intersection of sets (or a subset) of tests according to nose attributes

This command line executes only the basic tests for the index node configured in `my_config.ini` (basic set _intersect_ index 
set):
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic,index'
```
Note: You may provide as many attributes as you want (the operator is still _intersect_).

* Run a subset of tests without specified tests

This command line executes the basic tests for all types of node except the basic tests of the compute node:
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic,!compute'
```
* Run an union of sets of tests according to nose attributes

This example runs the union of the set of tests for the idp node and the set of tests for the index node (idp set _plus_ index 
set):
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a 'idp' -a 'index'
```
Note: You may provide as many '-a' expressions as you want (the operator is still _plus_).

Note: `-a '!compute' -a '!cog_create_user'` is helpless to avoid the tests for the compute node *and* the test case 'create 
user'.

* Run the tests located in a specified directory.

This example runs the tests located in test/test\_node\_components/test\_index (the tests for index node).
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini utils ./test/test_node_components/test_index
```
Note: the `utils` directory is mandatory (esgf-test-suite python libraries).

* Run tests, overriding the configuration

This example run the basic tests for index node, overring the index node value from the default configuration: it tests the index node of LLNL:
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file default.ini -a 'basic,index' --tc='nodes.index_node:esgf-node.llnl.gov'
```
Note: the `nodes.index_node` corresponds to the section `nodes` and the key `index_node` in the configuration file.

* Run tests without providing any configuration file:

This example runs the basic tests for the index node of LLNL:
```
python3 esgf-test.py -v --nocapture --nologcapture -a 'basic,index' --tc='nodes.index_node:esgf-node.llnl.gov'
```
More informations about the command line options concerning the configuration [here](https://pypi.python.org/pypi/nose-testconfig).

## Test selection

Attributes and set of test cases are described in ./esgf-test-suite/doc/plan\_test.pdf .

This pdf describes the sets of test cases by means of a mind map (or a tree). Each non-terminal node is a set of test cases.
For example the node labeled 'node\_components' is a set of test cases that is the union of the sets of test cases
corresponding to the nodes labeled 'compute', 'data', 'index' and 'idp' (fully recursive except for the terminal nodes).
The label of these nodes is the attribute to be referred to when you want to execute the corresponding set of test cases.

The terminal nodes are the test cases. they also have a label and they can be selectively executed but the label doesn't
correspond to their attribute. The attribute is composed of the label of the terminal node prefixed with the label of the
parent node, the name separator is the underscore.
For example the attribute for the http download test case (see data node) is 'dl\_http'.
This rule doesn't apply for the set of basic test cases (the parent node is labeled 'basic'): the basic test cases don't
have any attribute.

### Recommanded tests for a classical ESGF installation

* Without SLCS
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a '!compute,!cog_create_user,!slcs' --with-id
```

* With SLCS
```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a '!compute,!cog_create_user' --with-id
```

Don't forget to configure the superset to the value _classic_ in the configuration file.

### Recommanded tests for a ESGF docker deployement

```
python3 esgf-test.py -v --nocapture --nologcapture --tc-file my_config.ini -a 'basic,!compute' -a 'slcs' --with-id
```
Don't forget to configure the superset to the value _docker_ in the configuration file (see section Configuration).

## Remarks:

* This test suite needs to run and display an instance of Firefox. So if you run this test suite remotely, don't forget to enable X-Forwarding (ssh -Y or -X).
* This test suite can run with another browser than Firefox, provided a browser driver that will replace Geckodriver and modify your configuration file.
* Git ignores the geckodriver.log, my\_config\*.ini files and nosetests\*.html files.
* Do not use double quotes when specifying the nose attributes. Always use simple quotes.
* Esgf-test-suite/geckodriver/selenium don't work with version of Firefox less than 58.
* Don't make the Firefox window loose its focus when is_enable is set to True.

DISCLAIMER - the scripts in this repo are provided as is - use at your own risk - they have been tested only on a single system and may require modification to work correctly on other systems.
