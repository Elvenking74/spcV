import math
import tkinter, time, threading, sqlite3, datetime, json, functools
from tkinter import *

def funPomeraj():
    while True:
        global GLOB_COORDx, GLOB_COORDy
        can.move(ALL, (GLOB_COORDx.get()-NXTGLOB_COORDx.get())*6.45, (GLOB_COORDy.get()-NXTGLOB_COORDy.get())*7.2)
        GLOB_COORDx.set(NXTGLOB_COORDx.get())
        GLOB_COORDy.set(NXTGLOB_COORDy.get())

        time.sleep(0.05)

def funIspisSaz():
    for i in sazvezdjaTuple:
        lbx1.insert(0, str(i.idSaz) + "." + i.ime)

def funFilter():
    rez = list(filter(lambda x: x.getDist() < 150, zvezdeList))

    for i in rez:
        lbx.insert(0, "Ime: " + i.getIme() + " Distanca: " + str(i.getDist()))

def funRastojanje(zvz1, zvz2):
    ugao1 = abs(zvz1.x1 - zvz2.x1)/8

    lbx.insert(0, 'Ugao 1: ' + str(ugao1))
    lbx.insert(0, 'distanca 2: ' + str(zvz1.getDist()))
    lbx.insert(0, 'distanca 3: ' + str(zvz2.getDist()))
    stra1 = math.sqrt((zvz1.getDist()**2)+(zvz2.getDist()**2) - (2 * zvz1.getDist() * zvz2.getDist() * math.cos(ugao1)))
    lbx.insert(0, 'distanca izmedju '+ zvz1.getIme() + ' i ' + zvz2.getIme() + ' je: ' + str(int(stra1)))

def funZbirDist():
    listDist = []
    for i in zvezdeList:
        listDist.append(i.getDist())

    rez = functools.reduce(lambda x, y: x + y, listDist)

    lbx.insert(0, 'Zbir distanci je: ' + str(rez))

def updVreme():
    global vreme
    while True:
        now = datetime.datetime.now()
        vreme.set(now.strftime("%m/%d/%Y, %H:%M:%S"))
        time.sleep(1)

def funSacuvaj():
    dat = 'json.txt'
    fd = open(dat, 'w+')
    zvezdeDict = {}
    for i in zvezdeList:
        zvezdeDict = (i.to_json() + '\n')
        json.dump(zvezdeDict, fd)
        fd.write("\n")
    lbx.insert(0, 'Uspeo upis u ' + dat)
    fd.close()

def funMin(lista):
    pmc = lista[0]
    for i in lista:
        if i.getDist() < pmc.getDist():
            pmc = i

    lbx.insert(0, 'Minimalno rastojanje od zemlje ima: ' + pmc.getIme())

def funMax(lista):
    pmc = lista[0]
    for i in lista:
        if i.getDist() > pmc.getDist():
            pmc = i

    lbx.insert(0, 'Maksimalno rastojanje od zemlje ima: ' + pmc.getIme())

def funDist():
    rez = list(map(lambda x: x.getDist() * LY/SOS, zvezdeList))
    for i in range(len(rez)):
        lbx.insert(0, zvezdeList[i].getIme() + ':' + str(rez[i]) + ' Godina (343m/s)')



class zvezda():
    def __init__(self, x1, y1, rad, ime, dist, constel):
        self.x1 = x1
        self.y1 = y1
        self.coord = x1, y1, x1 + rad, y1 + rad
        self.ime = ime
        self.dist = dist
        self.constel = constel

    def getCoord(self):
        return self.coord

    def getDist(self):
        return self.dist

    def getIme(self):
        return self.ime

    def getSaz(self):
        return self.constel

    def __str__(self):
        return (self.ime + ' ' + ' ' + str(self.x1) + ' ' + str(self.y1) + ' ' + str(self.dist) + ' ' + str(self.constel))

    def to_json(self):
        return json.dumps(self.__dict__)

class saz():
    def __init__(self, idSaz, ime):
        self.idSaz = idSaz
        self.ime = ime

    def __str__(self):
        return str(self.idSaz) + ":" + self.ime


top = tkinter.Tk()
LY = 9.4 * (10**15)
SOS = 343

#Trenutne glob kordinante
GLOB_COORDx = IntVar() #MAX 360
GLOB_COORDy = IntVar() #MAX 360


#Sledece glob kordinante
NXTGLOB_COORDx = IntVar() #MAX 360
NXTGLOB_COORDy = IntVar() #MAX 360
NXTGLOB_COORDx.set(0)
NXTGLOB_COORDy.set(0)

#Size
top.geometry('1440x720')

#Kanvas
can = Canvas(top, bg='#000025', height='360', width='720')

#Konekcija open
conn = sqlite3.connect('sql/zvz.db')

#zvezde
zvezdeList = []
cursor = conn.execute("SELECT * FROM zvez, saz")
for row in cursor:
    zvezdeList.append(zvezda(row[1], row[2], row[3], row[0], row[4], row[-1]))

for a in zvezdeList:
    can.create_text(a.x1 + 15, a.y1 + 15, text=a.getIme(), fill='royal blue', font='14')
    can.create_oval(a.getCoord(), fill='white')

#sazvezdja
sazvezdjaTuple = ()
cursor = conn.execute("SELECT * FROM saz")

prov = True
while prov:
    sazList = []
    for row in cursor:
        sazList.append(saz(row[0], row[1]))

    sazvezdjaTuple = sazList
    prov = False



#Konekcija Close
conn.close()

#Strane sveta
can.create_text(1440, 1440, text='N', fill='red')
can.create_text(2160, 1440, text='E', fill='red')
can.create_text(2879, 1440, text='S', fill='red')
can.create_text(0, 1440, text='S', fill='red')
can.create_text(720, 1440, text='W', fill='red')

#kanvas
can.pack()

#Vreme
s = datetime.datetime.now()
vreme = StringVar()
vreme.set(s.strftime("%m/%d/%Y, %H:%M:%S"))
txtTime = Label(top, textvariable=vreme, foreground='yellow', bg='grey'); txtTime.place(x = 964, y = 5)

#Skale za x i y
scaley = Scale(top, variable=NXTGLOB_COORDy, background='silver', from_=0, to=359, length=358)
scaley.place(x=1081, y=0)
scalex = Scale(top, variable=NXTGLOB_COORDx, background='silver', from_=0, to=359, length= 718, orient=HORIZONTAL)
scalex.place(x=358, y=363)

#labele
lb1 = Label(top, textvariable=GLOB_COORDx)
lb1.place(x = 10, y = 0)
lb2 = Label(top, textvariable=GLOB_COORDy)
lb2.place(x = 10, y = 20)
lb3 = Label(top, textvariable=NXTGLOB_COORDx)
lb3.place(x = 10, y = 40)
lb4 = Label(top, textvariable=NXTGLOB_COORDy)
lb4.place(x = 10, y = 60)
top.update()

#button za json to txt
btn = Button(top, text='sacuvaj .json', bg='silver', command=funSacuvaj)
btn.place(x = 355, y = 420)

#filter, map, lambda, reduce
btn1 = Button(top, text='Min rastojanje od zemlje', bg='silver', command=lambda : funMin(zvezdeList))
btn1.place(x = 450, y = 420)

btn2 = Button(top, text='Max rastojanje od zemlje', bg='silver', command=lambda : funMax(zvezdeList))
btn2.place(x = 609, y = 420)

btn3 = Button(top, text='Speed of Light', bg='silver', command=funDist)
btn3.place(x = 770, y = 420)

btn4 = Button(top, text='Zvezde blize od 150ly', bg='silver', command=funFilter)
btn4.place(x = 880, y = 420)

btn5 = Button(top, text='Rastojanje izmedju zvezde ' + zvezdeList[0].getIme() + " i zvezde " + zvezdeList[1].getIme(), bg='silver', command=lambda : funRastojanje(zvezdeList[0], zvezdeList[1]))
btn5.place(x = 355, y = 470)

btn5 = Button(top, text='Zbir distanci od zemlje', bg='silver', command=funZbirDist)
btn5.place(x = 640, y = 470)

btn6 = Button(top, text='Sazvezdja', bg='black', fg='silver', command=funIspisSaz)
btn6.place(x = 790, y = 470)

lbInfo = Label(top, text='Scroll y to 60 and x to 180 for Ursa Minor')
lbInfo.place(x = 800, y = 700)

"""
#filter
ent1Str = StringVar(); ent1Str.set('1')
labelT1 = Label(top, text='Ukucajte brzinu (u ly)');labelT1.place(x = 355, y = 460)
ent1 = Entry(top, textvariable=ent1Str);ent1.place(x = 355, y = 490)
ent11 = IntVar(); ent11.set(zvezdeList[0].dist/int(ent1Str.get()))
label1 = Label(top, textvariable=ent11);label1.place(x = 480, y = 488)
"""

#lista
lbx = Listbox(top, width=50, height=44); lbx.place(x = 1130, y = 5)
lbx1 = Listbox(top, width=50, height=44); lbx1.place(x = 35, y = 5)

#NIT1
t1 = threading.Thread(target=funPomeraj, daemon=True)
t1.start()

#NIT2 == Vreme
t2 = threading.Thread(target=updVreme, daemon=True)
t2.start()

#cccccccccccccccccccccccccccccccccccccc
top.mainloop()


