# gui4annotate
A simple tool for annotating image data.

Requires Python3 (tested on 3.4, probably works on lower versions of Python3 as well) and GTK+, GDK and Cairo, all part of GObject Introspection API

You can get Python3 for Windows at https://www.python.org/downloads/windows/

For Windows, GObject Introspection library (Python bindings) can be obtained at https://sourceforge.net/projects/pygobjectwin32/files/
You want to download the file named `pygi-aio-<version>-setup.exe`. Minimal required version is 3.18. This installer has all you need for running GTK based apps written in Python (any version up to 3.4) on Windows. This app needs to have installed packages GObject, GTK+, GDK, GdkPixbuf and Cairo.

Don't forget you need to install Python before installing PyGI.

Then just run a script `gui.py`
