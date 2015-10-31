from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name = 'XSeriesTestTool',
      version = '0.1',
      description = 'A tool to help study and analyse NSW XSeries protocol compliant data blocks.',
      long_description = readme(),
      classifiers = [
          'Programming Language :: Python :: 3.4',
          'License :: OSI Approved :: GPLv3',
          'Development Status :: under constant development through feedback',
      ],
      keywords = 'Gambling Australia New South Wales NSW X XSeries XComm',
      url = 'https://github.com/nevtum/XSeriesTestTool',
      author = 'Neville Tummon',
      #author_email = 'nt.devs@gmail.com',
      license = 'GPLv3',
      packages = ['XSeriesTestTool'],
      install_requires = [
          'PyQt4',
          'sqlite3',
          'pyserial',
      ],
      include_package_data = True,
      zip_safe = False)
