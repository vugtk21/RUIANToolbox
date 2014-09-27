# -*- coding: utf-8 -*-
# File: notebook.py
#    http://docs.python.org/py3k/library/tkinter.ttk.html?highlight=ttk#notebook

from Tkinter import *
import ttk
from idlelib import ToolTip

class SetupForm(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('RÚIAN Toolbox - nastavení')
        self.createWidgets()
        self.editsRow = 0

    def createWidgets(self):
        demoPanel = Frame(self, name='ruiansetupform')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)

        nb = ttk.Notebook(demoPanel, name='notebook')
        nb.enable_traversal()
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)

        self.createDescriptionTab(nb)
        self.createDownloaderTab(nb)
        self.createImportTab(nb)
        self.createServicesTab(nb)

    def createDescriptionTab(self, nb):
        frame = ttk.Frame(nb, name='descrip')

        lbl = ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N,
                        text="Tato aplikace Vám umožní nastavit parametry komponent RÚIAN Toolbox.")

        # position and set resize behaviour
        lbl.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure((0,1), weight=1, uniform=1)

        # add to notebook (underline = index for short-cut character)
        nb.add(frame, text='Úvod ', underline=0, padding=2)

    def _say_neat(self, v):
        v.set('Yeah, I know...')
        self.update()
        self.after(500, v.set(''))

    def addControl(self, control, aColumn=0):
        control.grid(row=self.editsRow, column = aColumn, sticky=W)
        self.editsRow = self.editsRow + 1
        return control

    def addControlWithLabel(self, frame, control, caption):
        label = ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N, text=caption)
        label.grid(row=self.editsRow, column=0, sticky=E)
        control.grid(row=self.editsRow, column=1, sticky= W+E+N+S)
        self.editsRow += 1
        return control

    def createDownloaderTab(self, nb):
        frame = ttk.Frame(nb)

        self.editsRow = 0
        lbl = ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="RÚIAN Downloader umožňuje stáhnout aktuální databázi včetně stahování aktualizací.")
        lbl.grid(row=self.editsRow, column=0)
        self.editsRow += 1

        self.addControl(ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="Adresář se staženými daty:"))
        self.addControl(Entry(frame, bd=5))

        CheckVar1 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Rozbalit stažené soubory", variable = CheckVar1, onvalue = 1, offvalue = 0, width = 20))

        CheckVar2 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Spustit importér po stažení dat", variable = CheckVar2, onvalue = 1, offvalue = 0, width = 20))

        CheckVar4 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Ignorovat historická data", variable = CheckVar4, onvalue = 1, offvalue = 0, width = 20))

        CheckVar3 = IntVar()
        C1 = self.addControl(Checkbutton(frame, text = "Stahovat automaticky každý den", variable = CheckVar3, onvalue = 1, offvalue = 0, width = 20))

        self.addControl(ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="Čas stahování:"))
        b = self.addControl(Entry(frame, bd =5))
        ToolTip.ToolTip(b, 'Čas, ve který se mají stahovat denní aktualizace')

        self.editsRow += 1
        neatVar = StringVar()
        self.addControl(ttk.Button(frame, text='Stáhni data ', underline=0, command=lambda v=neatVar: self._say_neat(v)))

        nb.add(frame, text='Downloader ')

    def createImportTab(self, nb):
        frame = ttk.Frame(nb)
        lbl = ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N,
                         text="RÚIAN Importer umožňuje importovat stážený stav do databáze včetně načtení aktualizačních balíčků.")
        lbl.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)

        self.addControlWithLabel(frame, Entry(frame, bd=5), "Jméno databáze:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Host:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Uživatel:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Heslo:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Vrstvy:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Cesta k OS4Geo:")

        self.editsRow += 1
        neatVar = StringVar()
        self.addControl(ttk.Button(frame, text='Importuj ', underline=0, command=lambda v=neatVar: self._say_neat(v)), aColumn = 1)

        nb.add(frame, text='Importer ', underline=0)

    def createServicesTab(self, nb):
        frame = ttk.Frame(nb)
        lbl = ttk.Label(frame, wraplength='4i', justify=LEFT, anchor=N,
                text="RÚIAN Services umožňuje využívat repliku databáze RÚIAN pomocí standardizovaných služeb.")
        lbl.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)

        self.addControlWithLabel(frame, Entry(frame, bd=5), "Jméno serveru:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Port:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Cesta na server:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Database host:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Database port:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Database name:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "Database password:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "noCGIAppServerHTTP:")
        self.addControlWithLabel(frame, Entry(frame, bd=5), "noCGIAppPortNumber:")

        nb.add(frame, text='Services ', underline=0)

def center_window(w=300, h=200):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

if __name__ == '__main__':
    root = Tk()
    setupForm = SetupForm(root)
    center_window(500, 300)
    root.mainloop()

    #root = Tk()
    #root.wm_iconbitmap('C:\\Users\\raugustyn\\Desktop\\pyProject.png')
    #root.mainloop()



