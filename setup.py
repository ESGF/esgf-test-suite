from setuptools import setup, find_packages

setup(name='esgf-test-suite',
      version='2.3.0',
      description='Nose scripts for ESGF integration test and validation',
      url='http://github.com/ESGF/esgf-test-suite',
      author='Nicolas Carenton',
      author_email='nicolas.carenton@ipsl.jussieu.fr',
      maintainer='Sebastien Gardoll',
      maintainer_email='sebastien.gardoll@ipsl.fr',
      license='IPSL',
      packages=find_packages(),
      install_requires=[
          'nose',
          'pyopenssl',
	        'MyProxyClient',
	        'requests',
	        'lxml',
	        'selenium',
          'nose-testconfig',
          'nose-htmloutput'
      ],
      zip_safe=False,
      include_package_data=True)