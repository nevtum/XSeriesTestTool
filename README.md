XSeriesTestTool
===============

This tool helps in analysing and studying data blocks transmitted by
gaming machines that implement the NSW XSeries protocol.

To run in development mode, enter XSeriesTestTool/XSeriesTestTool/ from
the console, and type:

    $python app.py

Depends on PyQt4, PySerial, SQLite3.

Installation of dependencies
---------------

To install PySerial use Python's pip installer:

    $pip install pyserial

Usually Python comes with SQLite3 already installed. If not then use pip.

To install PyQt4 go to
http://www.riverbankcomputing.com/software/pyqt/download and download the
Python 3.4 installer. Currently only the 32-bit installer has been found
to be working.


Building an executable
---------------

In the console make sure PyInstaller is set up:

    $pip install pyinstaller
	
Build the executable:
	
	$pyinstaller --onefile app.py

Or without the annoying console output in the background:

    $pyinstaller --onefile --noconsole app.py

A 'dist' folder which contains the executable will be created after
compilation. Copy the 'gui' and 'settings' resource folders into the
'dist' folder. You should now be able to start the application and
run on other PCs without Python or other libraries installed.

Test Data Editor
---------------
XSeriesTestTool comes with a data editor to modify data that has been
recorded by XSeriesTestTool. This tool is currently in Alpha.

To run the editor enter XSeriesTestTool/XSeriesTestTool/ from the
console, and type:

    $python testdata_editor.py
