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

from distutils.core import setup
import py2exe

setup(
windows=[{"script": "app.py"}],
options={"py2exe":
{"dll_excludes": ["MSVCP90.dll"],
"includes": ["sip", "PyQt4.QtGui"]}}
)