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
 - globus-url-copy

Command for Red Hat / CentOS / Scientifix Linux:

     yum install python-devel openssl-devel libxml2-devel libxslt-devel globus-gass-copy-progs firefox


## Installation:

     pip install esgf-test-suite

## Configuration:

     vi [installation_dir]/esgf-test-suite/configuration.ini   

Modify the nodes section. If several nodes are specified, they all should be in the same federation. Account section do not need to be modified.  

## Usage:

     [installation_dir]/esgf-test-suite/runtests.sh
