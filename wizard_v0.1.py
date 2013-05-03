# -*- coding: utf-8 -*-

from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox,QTextBrowser,QPushButton)
from PyQt4.QtCore import (pyqtSlot, pyqtSignal, QRegExp, QObject)
import sys


class LicenseWizard(QWizard):
    NUM_PAGES = 6

    (PageIntro, PageImport, PageSetupDB, PageCreateDBStructure, PageImportParameters, PageImportDB) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(LicenseWizard, self).__init__(parent)

        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageImport, ImportPage())
        self.setPage(self.PageSetupDB, SetupDBPage())
        self.setPage(self.PageCreateDBStructure, CreateDBStructurePage())
        self.setPage(self.PageImportParameters, ImportParametersPage())
        self.setPage(self.PageImportDB, ImportDBPage())

        self.setStartId(self.PageIntro)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        #self.setOption(self.HaveHelpButton, True)
        #self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/logo.png"))

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr(u"Úvod"))
        #self.setPixmap(QWizard.WatermarkPixmap, QPixmap("cuzk.jpg"))
        topLabel = QLabel(self.tr(u'Tady bude neco napsaného <i>treba kurzívou</i> nebo <br>na novém rádku a <b style="font-size: large">tucne</b>,<br>protoze zde funguji HTML tagy.'))
        topLabel.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(topLabel)

        self.setLayout(layout)

    def nextId(self):
            return LicenseWizard.PageImport

class ImportPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportPage, self).__init__(parent)

        self.setTitle(self.tr(u"Vytvorení databázové struktury"))

        serverAddressLabel = QLabel("Adresa serveru: ")
        serverAddress = QLineEdit()
        serverAddressLabel.setBuddy(serverAddress)

        SQLPathLabel = QLabel(self.tr("Cesta k SQLPlus:"))
        SQLPath = QLineEdit()
        SQLPathLabel.setBuddy(SQLPath)

        userLabel = QLabel(self.tr(u"Uzivatel:"))
        user = QLineEdit()
        userLabel.setBuddy(user)

        passwordLabel = QLabel(self.tr("Heslo:"))
        password = QLineEdit()
        passwordLabel.setBuddy(password)

        grid = QGridLayout()
        grid.addWidget(serverAddressLabel, 0, 0)
        grid.addWidget(serverAddress, 0, 1)
        grid.addWidget(SQLPathLabel, 1, 0)
        grid.addWidget(SQLPath, 1, 1)
        grid.addWidget(userLabel, 2, 0)
        grid.addWidget(user, 2, 1)
        grid.addWidget(passwordLabel, 3, 0)
        grid.addWidget(password, 3, 1)
        self.setLayout(grid)

    def nextId(self):
        return LicenseWizard.PageSetupDB

class SetupDBPage(QWizardPage):
    def __init__(self, parent=None):
        super(SetupDBPage, self).__init__(parent)

        self.setTitle(self.tr(u"Nastavení vytvárené databáze"))
        #self.setSubTitle(self.tr("If you have an upgrade key, please fill in "
        #                         "the appropriate field."))

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

        nazvyObceLabel = QLabel(self.tr(u"Cásti obce"))
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
        return LicenseWizard.PageCreateDBStructure


class CreateDBStructurePage(QWizardPage):
    def __init__(self, parent=None):
        super(CreateDBStructurePage, self).__init__(parent)

        self.setTitle(self.tr(u"Vytvorení databázové struktury"))

        # setup the ui
        self._console = QTextBrowser(self)
        self._button  = QPushButton(self)
        self._button.setText('Test Me')

        def prepareSQL(status):
            if status == '0':
                return QLabel(self.tr(u"<font color=red>Pripraviji dávku SQL</font>"))
            else:
                return QLabel(self.tr(u"<font color=green>Pripraviji dávku SQL</font>"))

        def runSQL(status):
            if status == '0':
                return QLabel(self.tr(u"<font color=red>Spoustím dávku SQL</font>"))
            else:
                return QLabel(self.tr(u"<font color=green>Spoustím dávku SQL</font>"))

        def done(status):
            if status == '0':
                return QLabel(self.tr(u"<font color=red>Hotovo</font>"))
            else:
                return QLabel(self.tr(u"<font color=green>Hotovo</font>"))

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
        #print 'testing'
        #print 'testing2'

        # log some stuff
        logger.debug('Testing debug')
        logger.info('Testing info')
        logger.warning('Testing warning')
        logger.error('Testing error')

        # error out something
        #print blah


    def nextId(self):
        return LicenseWizard.PageImportParameters
        #return -1

class ImportParametersPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportParametersPage, self).__init__(parent)

        self.setTitle(self.tr("Parametry importu"))

        dirLabel = QLabel(self.tr(u"Adresár s daty RÚIAN"))
        setDir = QLineEdit()
        dirLabel.setBuddy(setDir)

        suffixLabel = QLabel(self.tr(u"Prípona souboru"))
        suffix = QLineEdit('.xml')
        suffixLabel.setBuddy(suffix)

        self.bottomLabel = QLabel()
        self.bottomLabel.setWordWrap(True)

        walkDir = QCheckBox(self.tr(u"Vcetne podadresáru"))

        #self.registerField("walkDir.agree*", walkDir)

        grid = QGridLayout()
        grid.addWidget(dirLabel, 0, 0)
        grid.addWidget(setDir, 0, 1)
        grid.addWidget(suffixLabel, 1, 0)
        grid.addWidget(suffix, 1, 1)
        grid.addWidget(self.bottomLabel, 2, 0)
        grid.addWidget(walkDir, 2, 1)

        self.setLayout(grid)

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


    def _configWizBtns(self, state):
        # position the Print button (CustomButton1) before the Finish button
        if state:
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.CustomButton1, QWizard.FinishButton,
                       QWizard.CancelButton]
            self.wizard().setButtonLayout(btnList)
        else:
            # remove it if it's not visible
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.FinishButton,
                       QWizard.CancelButton]
            self.wizard().setButtonLayout(btnList)


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

    #print 'Console..'

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()