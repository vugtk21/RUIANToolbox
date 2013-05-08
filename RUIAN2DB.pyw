# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        RUIAN2DB
# Purpose:
#
# Author:      DiblikT
#
# Created:     05/05/2013
# Copyright:   (c) DiblikT 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox,QTextBrowser,QPushButton, QIcon, QFileDialog)
from PyQt4.QtCore import (pyqtSlot, pyqtSignal, QRegExp, QObject, SIGNAL)
import sys,os
import configGUI as c
import importInterface

class LicenseWizard(QWizard):
    NUM_PAGES = 8

    (PageIntro, PageDatabaseType, PageTextFileDBHandler, PagePostGISDBHandler, PageSetupDB, PageCreateDBStructure, PageImportParameters, PageImportDB) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(LicenseWizard, self).__init__(parent)

        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageDatabaseType, DatabaseTypePage())
        self.setPage(self.PageTextFileDBHandler, TextFileDBHandlerPage())
        self.setPage(self.PagePostGISDBHandler, PostGISDBHandlerPage())
        self.setPage(self.PageSetupDB, SetupDBPage())
        self.setPage(self.PageCreateDBStructure, CreateDBStructurePage())
        self.setPage(self.PageImportParameters, ImportParametersPage())
        self.setPage(self.PageImportDB, ImportDBPage())

        self.setStartId(self.PageIntro)

        self.setWizardStyle(self.ModernStyle)
        self.setWindowTitle(u'EURADIN - Import RÚIAN')
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\pyProject.png')
        self.setWindowIcon(QIcon(self.pictureName))

        self.setButtonText(self.NextButton, QApplication.translate("LicenseWizard", 'Další >>', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.BackButton, QApplication.translate("LicenseWizard", '<< Zpět', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.CancelButton, QApplication.translate("LicenseWizard", 'Storno', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.FinishButton,QApplication.translate("LicenseWizard", 'Konec', None, QApplication.UnicodeUTF8))

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr(u"Úvod"))
        topLabel = QLabel()
        topLabel.setText(QApplication.translate("IntroPage", 'Tady bude neco napsaného <i>třeba kurzívou</i> nebo na <br> novém řádku a <b style="font-size: large">tučne</b>,<br>protože zde fungují HTML tagy.', None, QApplication.UnicodeUTF8))

        layout = QVBoxLayout()
        layout.addWidget(topLabel)

        self.setLayout(layout)

    def nextId(self):
            return LicenseWizard.PageDatabaseType

class DatabaseTypePage(QWizardPage):
    def __init__(self, parent=None):
        super(DatabaseTypePage, self).__init__(parent)

        self.setTitle(self.tr(u"Typ databáze"))
        self.textRBName = QApplication.translate("DatabaseTypePage", c.configData['databaseTypes']['textFile_DBHandler'], None, QApplication.UnicodeUTF8)
        self.pgRBName = QApplication.translate("DatabaseTypePage", c.configData['databaseTypes']['postGIS_DBHandler'], None, QApplication.UnicodeUTF8)
        self.textRB = QRadioButton(self.tr(self.textRBName), self)
        self.pgRB = QRadioButton(self.tr(self.pgRBName), self)
        self.pgRB.setChecked(True)

        #self.registerField("details.textRB*", self.textRB) or self.registerField("details.pgRB*", self.pgRB)

        grid = QGridLayout()
        grid.addWidget(self.textRB, 0, 0)
        grid.addWidget(self.pgRB, 1, 0)
        self.setLayout(grid)

    def nextId(self):
        if self.textRB.isChecked():
            return LicenseWizard.PageTextFileDBHandler
        else:
            return LicenseWizard.PagePostGISDBHandler

class TextFileDBHandlerPage(QWizardPage):
    def __init__(self, parent=None):
        super(TextFileDBHandlerPage, self).__init__(parent)

        self.setTitle(QApplication.translate("TextFileDBHandlerPage", 'Načtení databáze', None, QApplication.UnicodeUTF8))

        self.SQLPathLabel = QLabel(QApplication.translate("TextFileDBHandlerPage", 'Načíst z adresáře', None, QApplication.UnicodeUTF8))
        self.path = c.configData['textFile_DBHandler']['dataDirectory']
        self.SQLPath = QLineEdit(self.path)
        self.SQLPathLabel.setBuddy(self.SQLPath)

        self.openButton = QPushButton()
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\dir.png')
        self.openButton.setIcon(QIcon(self.pictureName))

        grid = QGridLayout()
        grid.addWidget(self.SQLPathLabel, 0, 0)
        grid.addWidget(self.SQLPath, 0, 1)
        grid.addWidget(self.openButton, 0, 2)
        self.setLayout(grid)

        self.connect(self.openButton, SIGNAL("clicked()"), self.setPath)

    def setPath(self):
        filedialog = QFileDialog.getExistingDirectory(self,QApplication.translate("TextFileDBHandlerPage", 'Výběr adresáře', None, QApplication.UnicodeUTF8))
        self.SQLPath.setText(filedialog)


    def nextId(self):
        return LicenseWizard.PageSetupDB

class PostGISDBHandlerPage(QWizardPage):
    def __init__(self, parent=None):
        super(PostGISDBHandlerPage, self).__init__(parent)

        self.setTitle(QApplication.translate("PostGISDBHandlerPage", 'Připojení databáze PostGIS', None, QApplication.UnicodeUTF8))

        dbNameLabel = QLabel("dbname")
        dbName = QLineEdit(c.configData['postGIS_DBHandler']['dbname'])
        dbNameLabel.setBuddy(dbName)

        hostLabel = QLabel("host")
        host = QLineEdit(c.configData['postGIS_DBHandler']['host'])
        hostLabel.setBuddy(host)

        portLabel = QLabel("port")
        port = QLineEdit(c.configData['postGIS_DBHandler']['port'])
        portLabel.setBuddy(port)

        userLabel = QLabel("user")
        user = QLineEdit(c.configData['postGIS_DBHandler']['user'])
        userLabel.setBuddy(user)

        passwordLabel = QLabel("password")
        password = QLineEdit(c.configData['postGIS_DBHandler']['password'])
        passwordLabel.setBuddy(password)

        schemaNameLabel = QLabel("schemaName")
        schemaName = QLineEdit(c.configData['postGIS_DBHandler']['schemaName'])
        schemaNameLabel.setBuddy(schemaName)

        grid = QGridLayout()
        grid.addWidget(dbNameLabel, 0, 0)
        grid.addWidget(dbName, 0, 1)
        grid.addWidget(hostLabel, 1, 0)
        grid.addWidget(host, 1, 1)
        grid.addWidget(portLabel, 2, 0)
        grid.addWidget(port, 2, 1)
        grid.addWidget(userLabel, 3, 0)
        grid.addWidget(user, 3, 1)
        grid.addWidget(passwordLabel, 4, 0)
        grid.addWidget(password, 4, 1)
        grid.addWidget(schemaNameLabel, 5, 0)
        grid.addWidget(schemaName, 5, 1)
        self.setLayout(grid)


    def nextId(self):
        return LicenseWizard.PageSetupDB

class SetupDBPage(QWizardPage):
    def __init__(self, parent=None):
        super(SetupDBPage, self).__init__(parent)

        self.setTitle(QApplication.translate("SetupDBPage", 'Sem patří treeView', None, QApplication.UnicodeUTF8))

        keyLabel = QLabel("<b>KEY<\b>")
        valueLable = QLabel("<b>value<\b>")

        tsLabel = QLabel("Table space")
        ts = QLineEdit('EURADIN_RUIAN')
        tsLabel.setBuddy(ts)

        schemaLabel = QLabel(self.tr("Database schema"))
        schema = QLineEdit('dbschema')
        schemaLabel.setBuddy(schema)

        obceLabel = QLabel(self.tr("Obce"))
        obce = QLineEdit('obce')
        obceLabel.setBuddy(obce)

        nazvyObceLabel = QLabel(QApplication.translate("SetupDBPage", 'Části obce', None, QApplication.UnicodeUTF8))
        nazvyObce = QLineEdit('casti_obce')
        nazvyObceLabel.setBuddy(nazvyObce)

        katUzLabel = QLabel(self.tr(u"Katastrální území"))
        katUz = QLineEdit('katastralni_uzemi')
        katUzLabel.setBuddy(katUz)

        uliceLabel = QLabel(self.tr("Ulice"))
        ulice = QLineEdit('ulice')
        uliceLabel.setBuddy(ulice)

        parcelyLabel = QLabel(self.tr("Parcely"))
        parcely = QLineEdit('parcely')
        parcelyLabel.setBuddy(parcely)

        stavObjLabel = QLabel(self.tr(u"Stavební objekty"))
        stavObj = QLineEdit('stavebni_objekty')
        stavObjLabel.setBuddy(stavObj)

        adrMistaLabel = QLabel(self.tr(u"Adresní místa"))
        adrMista = QLineEdit('adresni_mista')
        adrMistaLabel.setBuddy(adrMista)

        grid = QGridLayout()
        grid.addWidget(keyLabel, 0, 0)
        grid.addWidget(valueLable, 0, 1)
        grid.addWidget(tsLabel, 1, 0)
        grid.addWidget(ts, 1, 1)
        grid.addWidget(schemaLabel, 2, 0)
        grid.addWidget(schema, 2, 1)
        grid.addWidget(obceLabel, 3, 0)
        grid.addWidget(obce, 3, 1)
        grid.addWidget(nazvyObceLabel, 4, 0)
        grid.addWidget(nazvyObce, 4, 1)
        grid.addWidget(katUzLabel, 5, 0)
        grid.addWidget(katUz, 5, 1)
        grid.addWidget(uliceLabel, 6, 0)
        grid.addWidget(ulice, 6, 1)
        grid.addWidget(parcelyLabel, 7, 0)
        grid.addWidget(parcely, 7, 1)
        grid.addWidget(stavObjLabel, 8, 0)
        grid.addWidget(stavObj, 8, 1)
        grid.addWidget(adrMistaLabel, 9, 0)
        grid.addWidget(adrMista, 9, 1)
        self.setLayout(grid)

    def nextId(self):
        # Radecek
        if importInterface.databaseExists():
            return LicenseWizard.PageImportParameters
        else:
            return LicenseWizard.PageCreateDBStructure


class CreateDBStructurePage(QWizardPage):
    def __init__(self, parent=None):
        super(CreateDBStructurePage, self).__init__(parent)

        self.setTitle(QApplication.translate("CreateDBStructurePage", 'Vytvoření databázové struktury', None, QApplication.UnicodeUTF8))

        self._console = QTextBrowser(self)
        self._button  = QPushButton(self)
        self._button.setText('Test Me')

        def prepareSQL(status):
            if status == '0':
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=red>Připraviji dávku SQL</font>', None, QApplication.UnicodeUTF8))
            else:
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=green>Připraviji dávku SQL</font>', None, QApplication.UnicodeUTF8))

        def runSQL(status):
            if status == '0':
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=red>Spouštím dávku SQL</font>', None, QApplication.UnicodeUTF8))
            else:
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=green>Spouštím dávku SQL</font>', None, QApplication.UnicodeUTF8))

        def done(status):
            if status == '0':
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=red>Hotovo</font>', None, QApplication.UnicodeUTF8))
            else:
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=green>Hotovo</font>', None, QApplication.UnicodeUTF8))

        grid = QGridLayout()
        grid.addWidget(prepareSQL('1'), 0, 0)
        grid.addWidget(runSQL('0'), 1, 0)
        grid.addWidget(done('0'), 2, 0)
        grid.addWidget(self._console,3,0)
        grid.addWidget(self._button,6,0)
        self.setLayout(grid)

        # create connections
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        self._button.clicked.connect(self.test)

    def test( self ):
        # print some stuff
##        print 'testing'
##        print 'testing2'
##
##        # log some stuff
##        logger.debug('Testing debug')
##        logger.info('Testing info')
##        logger.warning('Testing warning')
##        logger.error('Testing error')
##
##        # error out something
##        print blah

        importInterface.createDatabase()


    def nextId(self):
        return LicenseWizard.PageImportParameters
        #return -1

class ImportParametersPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportParametersPage, self).__init__(parent)

        self.setTitle(self.tr("Parametry importu"))

        self.dirLabel = QLabel(QApplication.translate("ImportParametersPage", 'Adresář s daty RÚIAN', None, QApplication.UnicodeUTF8))
        self.setDir = QLineEdit()
        self.dirLabel.setBuddy(self.setDir)

        self.suffixLabel = QLabel(QApplication.translate("CreateDBStructurePage", 'Přípona souboru', None, QApplication.UnicodeUTF8))
        self.suffix = QLineEdit('.xml')
        self.suffixLabel.setBuddy(self.suffix)

        self.openButton1 = QPushButton()
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\dir.png')
        self.openButton1.setIcon(QIcon(self.pictureName))

        self.bottomLabel = QLabel()
        self.bottomLabel.setWordWrap(True)

        self.walkDir = QCheckBox(QApplication.translate("ImportParametersPage", 'Včetně podadresářů', None, QApplication.UnicodeUTF8))

        grid = QGridLayout()
        grid.addWidget(self.dirLabel, 0, 0)
        grid.addWidget(self.setDir, 0, 1)
        grid.addWidget(self.openButton1, 0, 2)
        grid.addWidget(self.suffixLabel, 1, 0)
        grid.addWidget(self.suffix, 1, 1)
        grid.addWidget(self.bottomLabel, 2, 0)
        grid.addWidget(self.walkDir, 2, 1)

        self.setLayout(grid)
        self.connect(self.openButton1, SIGNAL("clicked()"), self.setPath1)

    def setPath1(self):
        dirDialog = QFileDialog.getExistingDirectory(self, QApplication.translate("CreateDBStructurePage", 'Výběr adrešáře', None, QApplication.UnicodeUTF8))
        if not dirDialog.isNull():
            self.setDir.setText(dirDialog)

    def nextId(self):
        return LicenseWizard.PageImportDB

class ImportDBPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportDBPage, self).__init__(parent)

        self.setTitle(self.tr(u"Importování dat"))

        self._console = QTextBrowser(self)
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        grid = QGridLayout()
        grid.addWidget(self._console,0,0)
        self.setLayout(grid)

    def nextId(self):
        return -1

class XStream(QObject):
    _stdout = None
    _stderr = None

    messageWritten = pyqtSignal(str)

    def flush( self ):
        pass

    def fileno( self ):
        return -1

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


# main ========================================================================
def main():
    app = QApplication(sys.argv)
    wiz = LicenseWizard()
    wiz.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()