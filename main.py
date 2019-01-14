import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
from easygui import *
import os

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
    return V*np.cos(katNaRadiany(o))*t-(r*np.sin(katNaRadiany(o)))

def obliczaniePolozeniaY(k,r,a,m,t,V):
    return r*np.sin(katNaRadiany(90-o))+V*np.sin(katNaRadiany(o))*t-(9.80665*np.power(t,2))/2

def rysujWykres(t,x,y,c,v,nrProby):
    ax.plot(t[len(t) - 1], y[len(y) - 1], color='k')
    bx.plot(t[len(t) - 1], x[len(x) - 1], color='c')
    cx.plot(x[len(x) - 1], y[len(y) - 1], color='r')
    dx.plot(nrProby, c, color="m")
    ex.plot(t[len(t)-1],v[len(v)-1],color='y')
    fig.canvas.draw()

pygame.init()

T=0
k=0.1
r=5
o=45
m=100
deltaT = 0.001
myFont = pygame.font.Font("diablo_h.ttf", 18)
myFont2 = pygame.font.Font("diablo_h.ttf", 100)
fig = plt.figure(num=None,figsize=(8,6),dpi=100,facecolor='w',edgecolor='k')
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.5)
ax = fig.add_subplot(321)
ax.set_ylabel("y[m]")
ax.set_xlabel("t[s]")
bx = fig.add_subplot(322)
bx.set_ylabel("x[m]")
bx.set_xlabel("t[s]")
cx = fig.add_subplot(323)
cx.set_ylabel("y[m]")
cx.set_xlabel("x[m]")
dx = fig.add_subplot(324)
dx.set_ylabel("odległość od celu")
dx.set_xlabel("numer strzału")
ex = fig.add_subplot(325)
ex.set_ylabel("Vy[m\s]")
ex.set_xlabel("t[s]")
fig.show()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,100)
x = []
y = []
v = []
t =[]
c = []
nrProby=[]
startingDeegre=15
cel=[10,10.001]
stanPoprzedniegoStrzalu=0
########

msg = "Wpisz podstawowe parametry katapulty"
title = "Projekt Podstawy Automatyki - Katapulta STARAJĄCA się trafić do celu"
fieldNames = ["Długość ramienia", "Ustawienie klina", "Ciężar rzucanego obiektu","Współczynnik sprężystości","Odleglość od celu", "Szerokość celu"]
fieldValues = []
fieldValues = multenterbox(msg,title, fieldNames)


while 1:
  if fieldValues == None: break
  errmsg = ""
  for i in range(len(fieldNames)):
    if fieldValues[i].strip() == "":
      errmsg = errmsg + ('"%s" jest wymaganym polem.\n\n' % fieldNames[i])
    elif float(fieldValues[i])<=0:
        errmsg=errmsg+('"%s" musi być dodatnie! \n\n'% fieldNames[i])
  if errmsg == "": break
  fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
  if int(fieldValues[1])>=90 or int(fieldValues[1])<0:
      errmsg = errmsg + ('"%s" Wpisano złą wartość klina!.\n\n' % fieldNames[1])


r = float(fieldValues[0])
o = int(fieldValues[1])
m = int(fieldValues[2])
k = float(fieldValues[3])
a=(90-o)/2+o
cel[0]=float(fieldValues[4])
cel[1]=cel[0]+float(fieldValues[5])
#######
W=800
H=600
skala = 800/(1.2*cel[1])
screen = pygame.display.set_mode((W,H))
i=0
run = True
obraz2 = pygame.image.load("back.jpg")
obraz2 = pygame.transform.scale(obraz2, (800, 600))
screen.blit(obraz2, (0, 0))
while(run and startingDeegre>0 and a>o and a>=0 and a<=90):
    Vp = obliczaniePredkosci(k, r, a, o, m)
    v.append([])
    x.append([])
    y.append([])
    t.append([])
    T=0
    nrProby.append(i)
    i+=1
    while (True):
        for event in pygame.event.get():
            if event.type==pygame.KEYUP:
                if event.key==ord("z"):
                    deltaT*=2
                if event.key==ord("x"):
                    deltaT/=2
            elif event.type==pygame.QUIT:
                run=False
            else:
                pass
        if(not run):
            break
        T+=deltaT
        Y=obliczaniePolozeniaY(k, r, o, m, T,Vp)
        X=obliczaniePolozeniaX(k, r, o, m, T,Vp)
        V=Vp*np.sin(katNaRadiany(o))-9.80665*T
        v[len(v)-1].append(V)
        y[len(y)-1].append(Y)
        x[len(x)-1].append(X)
        t[len(t)-1].append(T)
        napis3 = myFont.render(str(a), 1, (0, 0, 0))
        napis = myFont.render("Obecna próbka czasu: "+str(deltaT)+"s.",1,(0,0,0))
        stan=""
        if(stanPoprzedniegoStrzalu==1):
            stan="PrzesTrzelił!"
        elif(stanPoprzedniegoStrzalu==-1):
            stan="NiedosTrzelił!"
        napis2 = myFont.render(stan, 1, (0, 0, 0))
        screen.blit(obraz2, (0, 0))
        screen.blit(napis3,[10,30])
        screen.blit(napis2, [10, 50])
        screen.blit(napis,[10,10])
        ball = pygame.draw.circle(screen, (255,13,255), (int(X*skala), H-int(Y*skala)), 10)
        grass = pygame.draw.line(screen, (100,100,100), (0, H - 1), (W , H - 1), 7)
        target= pygame.draw.line(screen,(255,0,0),(int(cel[0]*skala),H-1),(int(cel[1]*skala),H-1),7)
        pygame.display.update()

        if(Y<=0):
            break

    c.append(X - ((cel[0] + cel[1]) / 2))
    rysujWykres(t,x,y,c,v,nrProby)
    print("Stan poprzedniego strzalu: ",stanPoprzedniegoStrzalu,"StartingDeegre: ", startingDeegre,"\nnaciag: ", a,"klin: ",o, " zasieg",X, " wysokosc", Y)


    if (cel[0]<=x[len(x)-1][len(x[len(x)-1])-1] and x[len(x)-1][len(x[len(x)-1])-1]<=cel[1]):
        stanPoprzedniegoStrzalu=0
        screen.fill((255,255,255))
        obraz = pygame.image.load("509945.jpg")
        obraz = pygame.transform.scale(obraz,(800,600))
        screen.blit(obraz, (0,0))
        napis2 = myFont2.render("Trafiła!", 1, (255, 0, 0))
        screen.blit(napis2, [int(W/2)-266, int(H/2)-50])
        pygame.display.update()
        time.sleep(2)
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
            obrazx = pygame.image.load("not.jpg")
            obrazx = pygame.transform.scale(obrazx, (800, 600))
            screen.blit(obrazx, (0, 0))
            napis2 = myFont.render("Cel jest za daleko", 1, (255, 0, 0))
            screen.blit(napis2, [int(W / 2), int(H / 4)])
            pygame.display.update()
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
            obrazx = pygame.image.load("not.jpg")
            obrazx = pygame.transform.scale(obrazx, (800, 600))
            screen.blit(obrazx, (0, 0))
            napis2 = myFont.render("Cel jest za blisko!", 1, (255, 0, 0))
            screen.blit(napis2, [int(W / 2), int(H / 4)])
            pygame.display.update()
            break

running = True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        else:
            pass

plt.clf()