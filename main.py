import numpy as np
import matplotlib.pyplot as plt
import time
from decimal import Decimal
import pygame
from easygui import *


def fillData(wykres, typ):
    czas = []
    ilosc = []

    for i in range(len(wykres)):
        czas.append(wykres[i][0])
        ilosc.append(wykres[i][1])
    plt.plot(ilosc, czas, typ)

pozycjaXWCzasie = [[],[]]
pozycjaYWCzasie = []
def katNaRadiany(a):
    return np.deg2rad(a)
def obliczaniePredkosci(k,r,a,o,m):
    return np.sqrt((2*k*np.power((a-o)*r,2))/(m*np.power(r,2)))*r



def obliczaniePolozeniaX(k,r,a,m,t,V):
    return V*np.cos(katNaRadiany(o))*t

def obliczaniePolozeniaY(k,r,a,m,t,V):
    return r*np.sin(katNaRadiany(90-o))+V*np.sin(katNaRadiany(o))*t-(9.80665*np.power(t,2))/2

def rysujWykres(t,x,y):
    ax.plot(t[len(t) - 1], y[len(y) - 1], color='k')
    bx.plot(t[len(t) - 1], x[len(x) - 1], color='c')
    cx.plot(x[len(x) - 1], y[len(y) - 1], color='r')
    fig.canvas.draw()

T=0
k=0.1
r=5
a=90
o=45
m=100

"""
fig = plt.figure()
ax = fig.add_subplot(221)
bx = fig.add_subplot(222)
cx = fig.add_subplot(223)
fig.show()
"""
x = []
y = []
t =[]

startingDeegre=15
startingDeegreKlin=15
cel=[10,10.001]
stanPoprzedniKlina=0
stanPoprzedniegoStrzalu=0
########

msg = "Wpisz podstawowe parametry katapulty"
title = "Projekt Podstawy Automatyki - Katapulta STARAJĄCA się trafić do celu"
fieldNames = ["Długość ramienia", "Ustawienie klina", "Ciężar rzucanego obiektu","Współczynnik sprężystości","Odleglość od celu", "Szerokość celu"]
fieldValues = []  # we start with blanks for the values
fieldValues = multenterbox(msg,title, fieldNames)

# make sure that none of the fields was left blank
while 1:
  if fieldValues == None: break
  errmsg = ""
  for i in range(len(fieldNames)):
    if fieldValues[i].strip() == "":
      errmsg = errmsg + ('"%s" jest wymaganym polem.\n\n' % fieldNames[i])
  if errmsg == "": break # no problems found
  fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
r = float(fieldValues[0])
o = int(fieldValues[1])
m = int(fieldValues[2])
k = float(fieldValues[3])
cel[0]=float(fieldValues[4])
cel[1]=cel[0]+float(fieldValues[5])
#######
W=800
H=600
skala = 800/(1.2*cel[1])
screen = pygame.display.set_mode((W,H))
print(skala)
while(startingDeegre>0 and a>o and a>=0 and a<=90):
    V = obliczaniePredkosci(k, r, a, o, m)
    x.append([])
    y.append([])
    t.append([])
    T=0

    while (True):
        T+=0.001
        time.sleep(0.001)
        Y=obliczaniePolozeniaY(k, r, o, m, T,V)
        X=obliczaniePolozeniaX(k, r, o, m, T,V)
        y[len(y)-1].append(Y)
        x[len(x)-1].append(X)
        t[len(t)-1].append(T)
        screen.fill((255, 255, 255))
        ball = pygame.draw.circle(screen, (0, 0, 0), (int(X*skala), H-int(Y*skala)), 3)
        grass = pygame.draw.line(screen, (0, 255, 0), (0, H - 1), (W , H - 1), 4)
        target= pygame.draw.line(screen,(255,0,0),(int(cel[0]*skala),H-1),(int(cel[1]*skala),H-1),5)
        #print((int(cel[0]*skala),H-5),(int(cel[1]*skala),H-5),cel[0],skala)
        pygame.display.update()
        #rysujWykres(t, x, y)
        if(Y<=0):
            break
    print("Stan poprzedniego strzalu: ",stanPoprzedniegoStrzalu,"StartingDeegre: ", startingDeegre,"\nnaciag: ", a,"klin: ",o, " zasieg",X, " wysokosc", Y)


    if (cel[0]<=x[len(x)-1][len(x[len(x)-1])-1] and x[len(x)-1][len(x[len(x)-1])-1]<=cel[1]):
        stanPoprzedniegoStrzalu=0
        break

    elif cel[0]>x[len(x)-1][len(x[len(x)-1])-1]:
        print("1")
        if(stanPoprzedniegoStrzalu==1 or stanPoprzedniegoStrzalu==0):
            if (stanPoprzedniegoStrzalu != 0):
                startingDeegre/=2
            stanPoprzedniegoStrzalu=-1
        if(a+startingDeegre>90 and a!=90):
            a=90
        elif (a!=90):
            a+=startingDeegre
        else:
            break

    elif(cel[1]<x[len(x)-1][len(x[len(x)-1])-1]):
        print("2")
        if(stanPoprzedniegoStrzalu==-1 or stanPoprzedniegoStrzalu==0):
            if(stanPoprzedniegoStrzalu!=0):
                startingDeegre/=2
            stanPoprzedniegoStrzalu=1
        while(a-startingDeegre<=o):
            startingDeegre/=2
        if(a-startingDeegre<0 and a!=0):
            a=0
        elif(a!=0):
            a-=startingDeegre
        else:
            break
