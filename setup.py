from setuptools import setup

setup(name='esgf-test-suite',
      version='0.1',
      description='Nose scripts for ESGF integration test and validation',
      url='http://github.com/ESGF/esgf-test-suite',
      author='Nicolas Carenton',
      author_email='nicolas.carenton@ipsl.jussieu.fr',
      license='IPSL',
      packages=['esgf-test-suite'],
      install_requires=[
          'nose',
          'pyOpenSSL==0.13.1',
	  'MyProxyClient',
	  'requests',
	  'lxml',
	  'splinter',
      ],
      zip_safe=False,
      include_package_data=True)
