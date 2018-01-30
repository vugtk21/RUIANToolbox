# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import sys
from distutils.core import setup

PLATFORM_IS_WINDOWS = sys.platform.lower().startswith('win')

setup(
    name = "RUIANToolbox",
    version = "100",
    description = "Knihovna RUIAN Toolbox",
    author = "Radek Augustyn, Petr Liska, Tomas Vacek",
    author_email = "radek.augustyn@vugtk.cz",
    url = "https://github.com/vugtk21/RUIANToolbox",
    requires  = ['psycopg2 (>=2.5)', 'web (>=0.37)'],

    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found
    #recursively.)
    packages = [
        "downloader",
        "importer",
        "RUIANServices",
        "RUIANServices.services",
        "RUIANServices.testing",
        "sharedtools"
    ],

    # This is a list of files to install, and where (relative to the 'root' dir, where setup.py is.
    # You could be more specific.
    # 'package' package must contain files (see list above)
    # I called the package 'package' thus cleverly confusing the whole issue...
    # This dict maps the package name =to=> directories
    # It says, package *needs* these files.
    package_data = {
        "RUIANDownloader" : ["RUIANDownloader/*"],
        "RUIANDownloader" : ["RUIANImporter/*"],
        "RUIANServices"   : [
            "RUIANServices/*",
            "RUIANServices/HTML/*",
            "RUIANServices/img/*",
            "RUIANServices/soap/*"
        ],
        "sharedtools"     : ["sharedtools/*"]
    },

    #'RUIANToolbox.py' is in the root.
    scripts = ["RUIANToolbox.py"],
    long_description = """RÚIAN Toolbox je knihovna nástrojů a služeb, umožňující vytvářet a využívat kopie databáze Registru územní identifikace, adres a nemovitostí RÚIAN v prostředí sítě internetu, v prostředí počítačových sítí oddělených od internetu a v prostředí databází Client Server. Jednotlivé moduly knihovny pokrývají základní fáze životního cyklu repliky databáze RÚIAN s důrazem na využití adres, podporují automatické stahování dat ze serveru Veřejného dálkového přístupu (VDP), import stažených dat do geodatabáze a využívání adresních dat pomocí webových mapových služeb.
Všechny moduly jsou dostupné jako spustitelné aplikace včetně zdrojového kódu, zveřejněného jako OpenSource tak, aby mohly být jednotlivé komponenty na všech úrovních plnohodnotně začleněny do širších informačních technologií podle potřeby.
"""
)

if not PLATFORM_IS_WINDOWS:
    print "Delete BAT files."