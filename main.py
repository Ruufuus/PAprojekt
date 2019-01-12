import numpy as np
import matplotlib.pyplot as plt
import time
from decimal import Decimal
import pygame
import easygui


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
    return V*np.cos(katNaRadiany(a))*t

def obliczaniePolozeniaY(k,r,a,m,t,V):
    return r*np.sin(katNaRadiany(90-a))+V*np.sin(katNaRadiany(a))*t-(9.80665*np.power(t,2))/2

def rysujWykres(t,x,y):
    ax.plot(t[len(t) - 1], y[len(y) - 1], color='k')
    bx.plot(t[len(t) - 1], x[len(x) - 1], color='c')
    cx.plot(x[len(x) - 1], y[len(y) - 1], color='r')
    fig.canvas.draw()

T=0
k=0.1
r=5
a=90
o=50
m=1

fig = plt.figure()
ax = fig.add_subplot(221)
bx = fig.add_subplot(222)
cx = fig.add_subplot(223)
fig.show()
x = []
y = []
t =[]

startingDeegre=15
startingDeegreKlin=15
cel=[30,30.05]
stanPoprzedniKlina=0
stanPoprzedniegoStrzalu=0


while(startingDeegreKlin>0.0001 and o<=90 and o>=0):
    a=90
    startingDeegre=15
    while(startingDeegre>0.0001 and a>o and a>=0 and a<=90):
        V = obliczaniePredkosci(k, r, a, o, m)
        x.append([])
        y.append([])
        t.append([])
        T=0

        while (True):
            T+=0.5
            Y=obliczaniePolozeniaY(k, r, o, m, T,V)
            X=obliczaniePolozeniaX(k, r, o, m, T,V)
            y[len(y)-1].append(Y)
            x[len(x)-1].append(X)
            t[len(t)-1].append(T)
            rysujWykres(t,x,y)
            if(Y<=0):
                break


        print(stanPoprzedniegoStrzalu, startingDeegre, a,o, X)


        if (cel[0]<=x[len(x)-1][len(x[len(x)-1])-1] and x[len(x)-1][len(x[len(x)-1])-1]<=cel[1]):
            stanPoprzedniegoStrzalu=0
            break

        elif cel[0]>x[len(x)-1][len(x[len(x)-1])-1]:
            if(stanPoprzedniegoStrzalu==1 or stanPoprzedniegoStrzalu==0):
                if (stanPoprzedniegoStrzalu != 0):
                    startingDeegre/=2
                stanPoprzedniegoStrzalu=-1
            if(a+startingDeegre>90):
                a=90
            if (a!=90):
                a+=startingDeegre
            else:
                break

        elif(cel[1]<x[len(x)-1][len(x[len(x)-1])-1]):
            if(stanPoprzedniegoStrzalu==-1 or stanPoprzedniegoStrzalu==0):
                if(stanPoprzedniegoStrzalu!=0):
                    startingDeegre/=2
                stanPoprzedniegoStrzalu=1
            if(a-startingDeegre<0):
                a=0
            if(a!=0):
                a-=startingDeegre
            else:
                break

    if stanPoprzedniegoStrzalu==0:
        break

    elif a==0:
        if(stanPoprzedniKlina==1):
            startingDeegreKlin/=2
        stanPoprzedniKlina=-1

    elif a==90:
        if(stanPoprzedniKlina==-1):
            startingDeegre/=2
        stanPoprzedniKlina=1

