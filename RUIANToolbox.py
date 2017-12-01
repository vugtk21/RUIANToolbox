# -*- coding: utf-8 -*-


from Tkinter import *
import ttk
from idlelib import ToolTip

from downloader import downloadruian
from RUIANImporter import importRUIAN
from RUIANServices.services import config as RUIANServicesConfig

class SetupForm(Frame):
    tabFramesBorder = 10

    def _getFrame(self, aName):
        return Frame(self, name=aName, bd=5)

    def _getTopLabel(self, frame, description):
        #lbl = Label(frame, wraplength='4i', justify=LEFT, anchor=N, text=description)
        lbl = Text(frame, height=3, bd=0, wrap=WORD, font=self.customFont, bg="slate gray")
        lbl.insert(INSERT, description)
        lbl.config(state=DISABLED)
        #lbl.pack()
        lbl.grid(row=0, column=0, columnspan=2, sticky=W+E, pady=5)

    def __init__(self, root):
        import tkFont
        self.customFont = tkFont.Font(family="Helvetica", size=9)

        Frame.__init__(self, root)
        self.pack(expand=Y, fill=BOTH)

        self.master.title('RÚIAN Toolbox - nastavení')
        self.editsRow = 0
        self.createWidgets()

    def createWidgets(self):
        nb = ttk.Notebook(self, name='notebook')
        nb.enable_traversal()
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)

        self.createDescriptionTab(nb)
        self.createDownloaderTab(nb)
        self.createImportTab(nb)
        self.createServicesTab(nb)

        buttonsFrame = Frame(self, bd=5)
        btn = Button(buttonsFrame, text='Uložit konfiguraci a zavřít', underline=0)
        btn.pack(side = RIGHT, fill = BOTH)
        buttonsFrame.pack(side = BOTTOM, fill = BOTH)


    def createDescriptionTab(self, nb):
        frame = self._getFrame('descrip')

        self._getTopLabel(frame, "Tato aplikace umožňuje nastavit parametry komponent RÚIAN Toolbox.")

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure((0,1), weight=1, uniform=1)

        nb.add(frame, text='Úvod ', underline=0, padding=2)

    def _say_neat(self, v):
        v.set('Yeah, I know...')
        self.update()
        self.after(500, v.set(''))

    def addControl(self, control, aColumn=0, aSticky=W):
        control.grid(row=self.editsRow, column = aColumn, sticky=aSticky)
        self.editsRow = self.editsRow + 1
        return control

    def addControlWithLabel(self, frame, control, caption, editValue=""):
        label = Label(frame, wraplength='4i', justify=LEFT, anchor=N, text=caption)
        label.grid(row=self.editsRow, column=0, sticky=E)
        control.grid(row=self.editsRow, column=1, sticky=W+E+N+S)
        if editValue != "":
            control.insert(0, editValue)
        self.editsRow += 1
        return control

    def createDownloaderTab(self, nb):
        frame = self._getFrame("download")

        config = downloadruian.config

        self._getTopLabel(frame, "RÚIAN Downloader umožňuje stáhnout aktuální databázi včetně stahování aktualizací.")
        self.editsRow = 1

        self.addControl(Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="  Adresář se staženými daty:"))
        edit = self.addControl(Entry(frame, bd=1), aSticky=W+E)
        edit.insert(0, config.dataDir)

        CheckVar1 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Rozbalit stažené soubory", variable = CheckVar1, onvalue = 1, offvalue = 0))

        CheckVar2 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Spustit importér po stažení dat", variable = CheckVar2, onvalue = 1, offvalue = 0))

        CheckVar4 = IntVar()
        CheckVar4.set(1)#int(config.ignoreHistoricalData))
        C1 = self.addControl(Checkbutton(frame, text = "Ignorovat historická data", variable = CheckVar4, onvalue = 1, offvalue = 0))

        CheckVar3 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Stahovat automaticky každý den", variable = CheckVar3, onvalue = 1))

        self.addControl(Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="  Čas stahování:"))
        b = self.addControl(Entry(frame, bd=1), aSticky=W)
        b.insert(0, config.automaticDownloadTime)
        ToolTip.ToolTip(b, 'Čas, ve který se mají stahovat denní aktualizace')

        self.editsRow += 1

        neatVar = StringVar()
        self.addControl(Button(frame, text='Stáhni data ', underline=0, command=lambda v=neatVar: self._say_neat(v)), aSticky=E)

        frame.columnconfigure(0, weight=1, uniform=1)
        nb.add(frame, text='Downloader ')

    def createImportTab(self, nb):
        frame = self._getFrame("importTabFrame")
        config = importRUIAN.config

        self._getTopLabel(frame, "RÚIAN Importer umožňuje importovat stažený stav do databáze včetně načtení aktualizačních balíčků.")
        self.editsRow = 1

        self.addControlWithLabel(frame, Entry(frame, bd=1), "Jméno databáze:", editValue=config.dbname)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Host:", editValue=config.host)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Port:", editValue=config.port)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Uživatel:", editValue=config.user)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Heslo:", editValue=config.password)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Načítej pouze tyto vrstvy:", editValue=config.layers)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Cesta k OS4Geo:", editValue=config.os4GeoPath)

        self.editsRow += 1
        neatVar = StringVar()
        self.addControl(Button(frame, text='Importuj ', underline=0, command=lambda v=neatVar: self._say_neat(v)), aColumn = 1, aSticky=E)

        frame.columnconfigure(1, weight=1, uniform=1)
        nb.add(frame, text='Importer ', underline=0)

    def createServicesTab(self, nb):
        frame = self._getFrame("servicesTabFrame")
        config = RUIANServicesConfig.config

        self._getTopLabel(frame, "RÚIAN Services umožňuje využívat repliku databáze RÚIAN pomocí standardizovaných služeb.")
        self.editsRow = 1

        self.addControlWithLabel(frame, Entry(frame, bd=1), "Jméno serveru:", editValue=config.serverHTTP)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Port:", editValue=config.portNumber)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Cesta na server:", editValue=config.servicesWebPath)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Database host:", editValue=config.databaseHost)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Database port:", editValue=config.databasePort)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Database name:", editValue=config.databaseName)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Database user name:", editValue=config.databaseUserName)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "Database password:", editValue=config.databasePassword)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "noCGIAppServerHTTP:", editValue=config.noCGIAppServerHTTP)
        self.addControlWithLabel(frame, Entry(frame, bd=1), "noCGIAppPortNumber:", editValue=config.noCGIAppPortNumber)

        frame.columnconfigure(1, weight=1, uniform=1)
        nb.add(frame, text='Services ', underline=0)

def center_window(window, w=300, h=200):
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

if __name__ == '__main__':
    root = Tk()
    setupForm = SetupForm(root)
    center_window(root, 500, 350)
    root.mainloop()




