from distutils.core import setup
import py2exe

setup(
windows=[{"script": "app.py"}],
options={"py2exe":
{"dll_excludes": ["MSVCP90.dll"],
"includes": ["sip", "PyQt4.QtGui"]}}
)