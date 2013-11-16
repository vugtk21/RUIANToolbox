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
                         QMessageBox,QTextBrowser,QPushButton, QIcon, QFileDialog,QTreeWidget,QTreeWidgetItem, QProgressBar)
from PyQt4.QtCore import (pyqtSlot, pyqtSignal, QRegExp, QObject, SIGNAL, SLOT, Qt)
import sys,os
import configGUI as c
import importRUIAN

config = c.configData
messageConsole = None
_console1 = None
_console2 = None

def messageProc(message, tabLevel = 0):
    if messageConsole:
        tabStr = ""
        for i in range(0, tabLevel):
            tabStr = tabStr + "    "
        messageConsole.insertPlainText(tabStr + message + "\n")
    else:
        importRUIAN.dummyMessageProc(message, tabLevel)
    pass

importRUIAN.displayMessage = messageProc

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

        #self.setFixedSize(550,400)
        self.setWizardStyle(self.ModernStyle)
        self.setWindowTitle(u'EURADIN - Import RÚIAN')
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\pyProject.png')
        self.setWindowIcon(QIcon(self.pictureName))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  #  smazani tlacitka Help z

        self.setButtonText(self.NextButton, QApplication.translate("LicenseWizard", 'Další >>', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.BackButton, QApplication.translate("LicenseWizard", '<< Zpět', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.CancelButton, QApplication.translate("LicenseWizard", 'Storno', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.FinishButton,QApplication.translate("LicenseWizard", 'Konec', None, QApplication.UnicodeUTF8))

        self.prevId = None
        self.currentIdChanged.connect(self.onIdChanged)

    def onIdChanged(self, id):
        if self.prevId <> None and self.prevId < id:
            global messageConsole
            if id == 5:
                messageConsole = _console1
                XStream.stdout().messageWritten.connect( _console1.insertPlainText )
                XStream.stderr().messageWritten.connect( _console1.insertPlainText )

                importRUIAN.createDatabase(False)
            if id == 7:
                messageConsole = _console2
                XStream.stdout().messageWritten.connect( _console2.insertPlainText )
                XStream.stderr().messageWritten.connect( _console2.insertPlainText )
                importRUIAN.importDatabase()
        self.prevId = id

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr(u"Úvod"))
        self.topLabel = QLabel()
        self.topLabel.setWordWrap(True)
        self.topLabel.setText(QApplication.translate("IntroPage",
          'Tato aplikace umožňuje importovat vybraná data ' +
          '<a href="http://www.cuzk.cz/Dokument.aspx?PRARESKOD=998&MENUID=10769&AKCE=DOC:10-vybudovani-RUIAN">'
          'RÚIAN</a> ve výměnném formátu '+
          '<a href="http://www.cuzk.cz/Dokument.aspx?PRARESKOD=998&MENUID=10769&AKCE=DOC:10-VFR">VFR</a>'
          ' do geodatabáze. Datové soubory ' +
          'lze stahovat ze stránky ' +
          '<a href="http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej">' +
          'Veřejného dálkového přístupu</a>. Tyto soubory jsou volně ' +
          'dostupné ke stažení v komprimovaném archivu GZ, který je vhodné ' +
          'před použitím rozbalit.',
          None, QApplication.UnicodeUTF8))

        layout = QVBoxLayout()
        layout.addWidget(self.topLabel)

        self.setLayout(layout)

    def nextId(self):
            return LicenseWizard.PageDatabaseType

class DatabaseTypePage(QWizardPage):
    def __init__(self, parent=None):
        super(DatabaseTypePage, self).__init__(parent)

        self.setTitle(self.tr(u"Typ databáze"))
        self.textRB = QRadioButton(QApplication.translate("DatabaseTypePage", 'Databáze uložená jako textové soubory v adresáři', None, QApplication.UnicodeUTF8), None)
        self.pgRB = QRadioButton(QApplication.translate("DatabaseTypePage", 'Databáze PostGIS', None, QApplication.UnicodeUTF8), None)
        self.setCheckedButton()

        grid = QGridLayout()
        grid.addWidget(self.textRB, 0, 0)
        grid.addWidget(self.pgRB, 1, 0)

        self.setLayout(grid)

        self.connect(self.textRB, SIGNAL("clicked()"), self.updateDatabaseTypeText)
        self.connect(self.pgRB, SIGNAL("clicked()"), self.updateDatabaseTypePG)

    def setCheckedButton(self):
        dbType = config['selectedDatabaseType']
        if dbType == 'textFile_DBHandler':
            return self.textRB.setChecked(True)
        elif dbType == 'postGIS_DBHandler':
            return self.pgRB.setChecked(True)

    def updateDatabaseTypeText(self):
        config['selectedDatabaseType'] = 'textFile_DBHandler'

    def updateDatabaseTypePG(self):
        config['selectedDatabaseType'] = 'postGIS_DBHandler'

    def nextId(self):
        if self.textRB.isChecked():
            return LicenseWizard.PageTextFileDBHandler
        else:
            return LicenseWizard.PagePostGISDBHandler

class TextFileDBHandlerPage(QWizardPage):
    def __init__(self, parent=None):
        super(TextFileDBHandlerPage, self).__init__(parent)

        self.setTitle(QApplication.translate("TextFileDBHandlerPage", 'Parametry textové databáze', None, QApplication.UnicodeUTF8))

        self.SQLPathLabel = QLabel(QApplication.translate("TextFileDBHandlerPage", 'Adresář k uložení databáze', None, QApplication.UnicodeUTF8))
        self.path = config['textFile_DBHandler']['dataDirectory']
        self.SQLPath = QLineEdit(self.path)
        self.SQLPathLabel.setBuddy(self.SQLPath)
        self.SQLPath.textChanged[str].connect(self.updateSQLPath)

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

    def updateSQLPath(self, value):
        config['textFile_DBHandler']['dataDirectory'] = str(value)

    def setPath(self):
        filedialog = QFileDialog.getExistingDirectory(self,QApplication.translate("TextFileDBHandlerPage", 'Výběr adresáře', None, QApplication.UnicodeUTF8))
        self.SQLPath.setText(filedialog)


    def nextId(self):
        importRUIAN.createDatabaseHandler()
        if importRUIAN.databaseHandler.databaseExists():
            return LicenseWizard.PageImportParameters
        else:
            return LicenseWizard.PageSetupDB
        pass

class PostGISDBHandlerPage(QWizardPage):
    def __init__(self, parent=None):
        super(PostGISDBHandlerPage, self).__init__(parent)

        self.setTitle(QApplication.translate("PostGISDBHandlerPage", 'Parametry připojení do databáze PostGIS', None, QApplication.UnicodeUTF8))

        dbNameLabel = QLabel("dbname")
        dbName = QLineEdit(config['postGIS_DBHandler']['dbname'])
        dbNameLabel.setBuddy(dbName)
        dbName.textChanged[str].connect(self.updatedbName)

        hostLabel = QLabel("host")
        host = QLineEdit(config['postGIS_DBHandler']['host'])
        hostLabel.setBuddy(host)
        host.textChanged[str].connect(self.updateHost)

        portLabel = QLabel("port")
        port = QLineEdit(config['postGIS_DBHandler']['port'])
        portLabel.setBuddy(port)
        port.textChanged[str].connect(self.updatePort)

        userLabel = QLabel("user")
        user = QLineEdit(config['postGIS_DBHandler']['user'])
        userLabel.setBuddy(user)
        user.textChanged[str].connect(self.updateUser)

        passwordLabel = QLabel("password")
        password = QLineEdit(config['postGIS_DBHandler']['password'])
        passwordLabel.setBuddy(password)
        password.textChanged[str].connect(self.updatePassword)

        schemaNameLabel = QLabel("schemaName")
        schemaName = QLineEdit(config['postGIS_DBHandler']['schemaName'])
        schemaNameLabel.setBuddy(schemaName)
        schemaName.textChanged[str].connect(self.updateSchemaName)

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

    def updatedbName(self, value):
        config['postGIS_DBHandler']['dbname'] = str(value)

    def updateHost(self, value):
        config['postGIS_DBHandler']['host'] = str(value)

    def updatePort(self, value):
        config['postGIS_DBHandler']['port'] = str(value)

    def updateUser(self, value):
        config['postGIS_DBHandler']['user'] = str(value)

    def updatePassword(self, value):
        config['postGIS_DBHandler']['password'] = str(value)

    def updateSchemaName(self, value):
        config['postGIS_DBHandler']['schemaName'] = str(value)

    def nextId(self):
        return LicenseWizard.PageSetupDB

class SetupDBPage(QWizardPage):

    treeViewSetting = config['treeViewSet']

    def __init__(self, parent=None):
        super(SetupDBPage, self).__init__(parent)

        self.setTitle(QApplication.translate("SetupDBPage", 'Importované tabulky a sloupce', None, QApplication.UnicodeUTF8))

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.addItems(self.treeWidget.invisibleRootItem())
        self.treeWidget.itemChanged.connect (self.checkBoxDriver)
        self.treeWidget.itemChanged.connect (self.rewriteConfig)

        layout = QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

    def addItems(self, parent):
        column = 0
        names = self.treeViewSetting.keys()
        for name in names:
            if 'Root' not in name:
                nameParent = name
                statusParent = self.treeViewSetting[name + 'Root']
                nameParent = self.addParent(parent, column, str(name), 'data ' + str(name), statusParent)
                atribs = self.treeViewSetting[name].keys()
                for atr in atribs:
                    statusAtr = self.treeViewSetting[name][atr]
                    self.addChild(nameParent, column,str(atr),'data ' + str(atr), statusAtr)

    def addParent(self, parent, column, title, data, status):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setCheckState (column, self.getCheckStatus(status))
        item.setExpanded (False)
        return item

    def addChild(self, parent, column, title, data, status):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        item.setCheckState (column, self.getCheckStatus(status))
        return item

    def getCheckStatus(self,status):
        if status == 'True':
            return Qt.Checked
        if status == 'Semi':
            return Qt.PartiallyChecked
        if status == 'False':
            return Qt.Unchecked

    def checkBoxDriver(self, item, column):
        if self.hasParent(item, column) == False:  #  zmenou u rodice se zmeni i vsechny deti
            myChildCount = item.childCount()
            for i in range (0, myChildCount):
                myChild = item.child(i)
                myChild.setCheckState (column, item.checkState(column))

    def hasParent(self, item, column):
        try:
            parent =  item.parent()
            parent.text(column)
            return True
        except:
            return False

    def rewriteConfig(self, item, column):
        parent =  item.parent()
        itemText = str(item.text(column))
        if self.hasParent(item, column) == True:                    #  = nazev tabulky
            parentText = str(parent.text(column))
            if item.checkState(column) == Qt.Checked:
                config['treeViewSet'][parentText][itemText] = 'True'
            if item.checkState(column) == Qt.Unchecked:
                config['treeViewSet'][parentText][itemText] = 'False'

        else:              #  = nazev atributu
            if item.checkState(column) == Qt.Checked:
                config['treeViewSet'][itemText + 'Root'] = 'True'
            if item.checkState(column) == Qt.PartiallyChecked:
                config['treeViewSet'][itemText + 'Root'] = 'Semi'
            if item.checkState(column) == Qt.Unchecked:
                config['treeViewSet'][itemText + 'Root'] = 'False'


    def nextId(self):
        if importRUIAN.databaseExists():
            return LicenseWizard.PageImportParameters
        else:
            return LicenseWizard.PageCreateDBStructure


class CreateDBStructurePage(QWizardPage):
    def __init__(self, parent=None):
        super(CreateDBStructurePage, self).__init__(parent)

        self.setTitle(QApplication.translate("CreateDBStructurePage", 'Vytvoření databázové struktury', None, QApplication.UnicodeUTF8))

        self._console = QTextBrowser(self)

        global _console1
        _console1 = self._console

        grid = QGridLayout()
        grid.addWidget(self._console,3,0)

        #self.porcessProgressBar = QProgressBar()
        #self.porcessProgressBar.setMaximum(100)

        #self.porcessProgressBar.setProperty("value", 10)
        #self.porcessProgressBar.setValue(50)
        #self.porcessProgressBar.setTextVisible(False)
        #self.porcessProgressBar.setObjectName(_fromUtf8("porcessProgressBar"))
        #grid.addWidget(self.porcessProgressBar)

        self.setLayout(grid)

        #self._console.insertPlainText("ahoj")
        # create connections
        #XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        #XStream.stderr().messageWritten.connect( self._console.insertPlainText )

    def nextId(self):
        return LicenseWizard.PageImportParameters

class ImportParametersPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportParametersPage, self).__init__(parent)

        self.setTitle(self.tr("Parametry importu"))

        self.dirLabel = QLabel(QApplication.translate("ImportParametersPage", 'Adresář s daty RÚIAN', None, QApplication.UnicodeUTF8))
        self.setDir = QLineEdit(config['importParameters']['dataRUIANDir'])
        self.dirLabel.setBuddy(self.setDir)
        self.setDir.textChanged[str].connect(self.updateDir)

        self.suffixLabel = QLabel(QApplication.translate("CreateDBStructurePage", 'Přípona souboru', None, QApplication.UnicodeUTF8))
        self.suffix = QLineEdit(config['importParameters']['suffix'])
        self.suffixLabel.setBuddy(self.suffix)
        self.suffix.textChanged[str].connect(self.updateSuffix)

        self.openButton1 = QPushButton()
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\dir.png')
        self.openButton1.setIcon(QIcon(self.pictureName))

        self.walkDir = QCheckBox(QApplication.translate("ImportParametersPage", 'Včetně podadresářů', None, QApplication.UnicodeUTF8))

        if config['importParameters']['subDirs'] == 'True':
            self.walkDir.setCheckState(Qt.Checked)
        else:
            self.walkDir.setCheckState(Qt.Unchecked)

        self.walkDir.stateChanged[int].connect(self.updateSubDirs)

        grid = QGridLayout()
        grid.addWidget(self.dirLabel, 0, 0)
        grid.addWidget(self.setDir, 0, 1)
        grid.addWidget(self.openButton1, 0, 2)
        grid.addWidget(self.suffixLabel, 1, 0)
        grid.addWidget(self.suffix, 1, 1)
        grid.addWidget(self.walkDir, 2, 1)

        self.setLayout(grid)
        self.connect(self.openButton1, SIGNAL("clicked()"), self.setPath1)

    def updateDir(self, value):
        config['importParameters']['dataRUIANDir'] = str(value)

    def updateSuffix(self, value):
        config['importParameters']['suffix'] = str(value)

    def updateSubDirs(self, value):
        if value == 2:
            config['importParameters']['subDirs'] = 'True'
        else:
            config['importParameters']['subDirs'] = 'False'

    def setPath1(self):
        dirDialog = QFileDialog.getExistingDirectory(self, QApplication.translate("CreateDBStructurePage", 'Výběr adrešáře', None, QApplication.UnicodeUTF8))
        if not dirDialog.isNull():
            self.setDir.setText(dirDialog)

    def nextId(self):
        return LicenseWizard.PageImportDB

class ImportDBPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportDBPage, self).__init__(parent)

        self.setTitle(self.tr(u"Import"))

        self._console = QTextBrowser(self)
        global _console2
        _console2 = self._console
        #XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        #XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        grid = QGridLayout()
        grid.addWidget(self._console,0,0)

        #self.porcessProgressBar = QProgressBar()
        #self.porcessProgressBar.setMaximum(100)

        #self.porcessProgressBar.setProperty("value", 10)
        #self.porcessProgressBar.setValue(50)
        #self.porcessProgressBar.setTextVisible(False)
        #self.porcessProgressBar.setObjectName(_fromUtf8("porcessProgressBar"))
        #grid.addWidget(self.porcessProgressBar)

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

class Save():
    def saveNewConfig(self):
        f = open('configGUI.py','w')
        newText = '# -*- coding: utf-8 -*-\nconfigData = ' + str(config)
        newText = newText.encode("utf-8")
        f.write(newText)
        f.close()
        print 'Config file saved.'

# main ========================================================================
def saveAndExit(app):
    if app.exec_() == 0:
        s = Save()
        s.saveNewConfig()
        return 0
    else:
        app.exec_()

def main():
    app = QApplication(sys.argv)
    wiz = LicenseWizard()
    wiz.show()

    sys.exit(saveAndExit(app))

if __name__ == '__main__':
    main()