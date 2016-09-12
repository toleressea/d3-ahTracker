import os
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.tix import *
from tkinter import messagebox
from tkinter import font
            
root = Tk()
root.title('AH Calculator')
            
class dbfHandler:
   
   def __init__(self,dbfLoc):
      self.conn = sqlite3.connect(dbfLoc)
      self.c = self.conn.cursor()
      
      self.c.execute(
         '''CREATE TABLE IF NOT EXISTS trans (date, type, amount INT)'''
         )
      
      self.conn.commit()
      
   def insertTrans(self):
      (d, t, a) = (dateVar.get(), typeVar.get(), amountVar.get())
      if len(d) < 1 or len(t) < 1 or len(a) < 1:
         messagebox.showerror(title='Field Empty', message='Please fill out all empty fields.')
      else:
         self.c.execute(
            '''INSERT INTO trans VALUES('{date}', '{type}', {amount})'''.format(
               date=d,
               type=t,
               amount=int(a)
               )
            )
         self.conn.commit()
         amountEntry['validate'] = 'focus'
         refresh()
         
   def getTotal(self, t):
      self.c.execute(
         '''SELECT amount FROM trans WHERE type="{0}"'''.format(t)
         )
      values = self.c.fetchall()
      sum = 0
      for val in values:
         sum += val[0]
      return sum
      
   def showAll(self):
      self.c.execute('''SELECT * FROM trans ORDER BY {0}'''.format(orderVar.get()))
      all = self.c.fetchall()
      
      x = '{0}{1}{2}\n\n'.format('Date'.ljust(15), 'Type'.ljust(15), 'Amount'.ljust(15))
      for i in all:
         x += '{0}{1}{2}\n'.format(i[0].ljust(15), i[1].ljust(15), i[2])
      
      return x
      
dbf = dbfHandler('ahCalcHistory.db')
      
def refresh(*args):
   spentVar.set(dbf.getTotal('Bought'))
   grossVar.set(dbf.getTotal('Sold'))
   profitVar.set(grossVar.get() - spentVar.get())
   blizVar.set(round((grossVar.get()/0.85)-grossVar.get() + (spentVar.get() * 0.15)))
   x.set(dbf.showAll())
      
dateVar = StringVar()
orderVar = StringVar()
typeVar = StringVar()
amountVar = StringVar()
grossVar = IntVar()
spentVar = IntVar()
blizVar = IntVar()
profitVar = IntVar()

orderVar.set('Date')
typeVar.set('Bought')
dateVar.set('yyyymmdd')
x = StringVar()
x.set('')
      
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

addFrame = ttk.Frame(root, padding=(5, 5, 5, 5))
addFrame.grid(column=0, padx=15, row=0, sticky=(N, W, E, S))
statFrame = ttk.Frame(root, padding=(5, 5, 5, 5))
statFrame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
listFrame = ttk.Frame(root, padding=(5, 5, 5, 5))
listFrame.grid(column=1, row=0, rowspan=2)

dateTitle = ttk.Label(addFrame, text='Date: ').grid(column=0, row=0, sticky=(W))
typeTitle = ttk.Label(addFrame, text='Type: ').grid(column=0, row=1, sticky=(W))
amountTitle = ttk.Label(addFrame, text='Amount: ').grid(column=0, row=2, sticky=(W))
addBtn = ttk.Button(addFrame, text='Add Transaction', command=dbf.insertTrans).grid(column=0,row=3, columnspan=2, sticky=(W, E))

dateEntry = ttk.Entry(addFrame, width=11, textvariable=dateVar).grid(column=1, row=0, sticky=(E))
typeEntry = ttk.Combobox(addFrame, width=8, textvariable=typeVar, values=('Bought', 'Sold')).grid(column=1, row=1, sticky=(E))
amountEntry = ttk.Entry(addFrame, width=11, textvariable=amountVar)
amountEntry.grid(column=1, row=2, sticky=(E))

grossTitle = ttk.Label(statFrame, text='Total Income').grid(column=0, row=0, sticky=(W))
spentTitle = ttk.Label(statFrame, text='Total Spent').grid(column=2, row=0, sticky=(W))
statSep = ttk.Separator(statFrame, orient=VERTICAL).grid(column=1, row=0, rowspan=10, sticky=(N, S))
grossVal = ttk.Label(statFrame, textvariable=grossVar).grid(column=0, row=1, sticky=(E, W))
spentVal = ttk.Label(statFrame, textvariable=spentVar).grid(column=2, row=1, sticky=(E, W))

profitTitle = ttk.Label(statFrame, text='Total Profit').grid(column=0, row=3, sticky=(W))
blizTitle = ttk.Label(statFrame, text="Blizzard's 15%").grid(column=2, row=3, sticky=(W))
statSep = ttk.Separator(statFrame, orient=HORIZONTAL).grid(column=0, row=2, columnspan=10, sticky=(E, W))
profitVal = ttk.Label(statFrame, textvariable=profitVar).grid(column=0, row=4, sticky=(E, W))
blizVal = ttk.Label(statFrame, textvariable=blizVar).grid(column=2, row=4, sticky=(E, W))

orderByLbl = ttk.Label(listFrame, text='Order By: ').grid(padx=100, column=1, row=0, sticky=(E))
orderByCombo = ttk.Combobox(listFrame, width=10, textvariable=orderVar, values=('Date', 'Type', 'Amount'))
orderByCombo.grid(column=1, row=0, sticky=(E))

swinFont = font.Font(family='Consolas', size='8')
swin = ScrolledWindow(listFrame, width=300, height=250)
swin.grid(column=0,row=2, columnspan=2)
descript = swin.window
ttk.Label(descript, textvariable=x, font = swinFont).grid(column=0, row=0)

orderByCombo.bind('<<ComboboxSelected>>', refresh)

refresh()

if __name__ == '__main__':
   root.mainloop()