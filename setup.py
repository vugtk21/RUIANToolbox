__author__ = 'raugustyn'

import sys
from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["RUIANDownloader/*", "RUIANImporter/*", "RUIANServices/*", "SharedTools/*"]

PLATFORM_IS_WINDOWS = sys.platform.lower().startswith('win')


setup(
    name = "RUIANToolbox",
    version = "100",
    description = "RUIAN Toolbox",
    author = "Radek Augustyn, Petr Liska, Tomas Diblik, Tomas Vacek",
    author_email = "radek.augustyn@vugtk.cz",
    url = "https://github.com/vugtk21/RUIANToolbox",
    install_requires  = ['psycopg2>2.5', 'web>0.37'],

    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found
    #recursively.)
    packages = ['RUIANDownloader', "RUIANImporter", "RUIANServices", "SharedTools"],

    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'package' : files },

    #'RUIANToolbox.py' is in the root.
    scripts = ["RUIANToolbox.py"],
    long_description = """RUIAN Toolbox."""
)