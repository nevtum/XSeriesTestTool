"""
XSeriesTestTool - A NSW gaming protocol decoder/analyzer
    Copyright (C) 2012  Neville Tummon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name = 'XSeriesTestTool',
      version = '0.1',
      description = 'A tool to help study and analyse NSW XSeries protocol compliant data blocks.',
      long_description = readme(),
      classifiers = [
          'Programming Language :: Python :: 2.7',
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
