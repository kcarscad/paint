# name: 'paint.py'
# author: keith carscadden
# date: 5/23/14
# purpose: make a multifunctional paint program

import math,sys,time,pygame as pg
from random import randint
from pygame.locals import *
from ColorTile import ColorTile
from ShapeTile import ShapeTile
from OutlineTile import OutlineTile
from Slider import Slider

def randCol():
    return randint(0,255),randint(0,255),randint(0,255)


# ######################## SETUP ######################## #

# constants
PADDING = 25
SIZE = 8
BG = (240,240,240)
HL = (255,127,0)

# time stamping
def dateStr():
    year,mon,mday,hour,mins,sec,wday,yday,isDST = time.localtime()
    dateStr = '{}_{}_{}_{}h{}m{}s'.format(year,['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'][mon-1],mday,hour,mins,sec)
    return dateStr


# create 'colorTiles' objects
clrs = [(0,0,0),(64,64,64),(127,127,127),(191,191,191),(255,255,255),
        (255,0,0),(0,255,0),(0,0,255),
        (255,255,0),(255,0,255),(0,255,255),
        (0,127,255),(127,0,255),(255,0,127),
        (255,127,0),(127,255,0),(0,255,127),
        (255,255,127),(255,127,255),(127,255,255)]
colorTiles = []

W = 40

across,p,w,h = 5,5,W,W
for n,c in enumerate(clrs):
    obj = ColorTile(c,[p+(w+p)*(n%across),p+(w+p)*int(n/across),w,h],False)
    colorTiles.append(obj)
colorHeight = math.ceil((len(clrs)*1.0)/across)*(h+p) + p

# select first color, make LEFT_BOUND
LEFT_BOUND = across*w+(across+1)*p


# create 'sliders' objects
x,y,w,h = 5,colorHeight+PADDING,LEFT_BOUND-10,10
r = Slider(x,y,w,h,0)
g = Slider(x,y+15,w,h,1)
b = Slider(x,y+30,w,h,2)
sizeSlider = Slider(x,y+140,w,h,3)
sliders = [r,g,b,sizeSlider]


# create 'shapeTiles' objects
shapeTiles = []
across = 4
p,w,h = 5,(LEFT_BOUND-(across+1)*p)/(across*1.0),W
for i in range(across):
    obj = ShapeTile(i,[p+(w+p)*(i%across),colorHeight+PADDING+225+p+(w+p)*int(i/across),w,h],False)
    shapeTiles.append(obj)
shapeTiles[0].selected(True)


# create 'outlineTiles' objects
outlineTiles = []
across = 2
p,w,h = 5,(LEFT_BOUND-(across+1)*p)/(across*1.0),40
for i in range(across):
    obj = OutlineTile([p+(w+p)*(i%across),colorHeight+PADDING+300+p+(w+p)*int(i/across),w,h],False)
    outlineTiles.append(obj)
outlineTiles[0].selected(True)


# create 'specialTiles objects
specialTiles = []
across=3
p,w,h = 5,(LEFT_BOUND-(across+1)*p)/(across*1.0),W
for i in range(across):
    obj = OutlineTile([p+(w+p)*(i%across),colorHeight+PADDING+375+p+(w+p)*int(i/across),w,h],False)
    obj.setType('specialtile')
    specialTiles.append(obj)


# surface(s) init
#   paintRect: paint area
# controlRect: controls area
pg.init()
size = width, height = 800+LEFT_BOUND,800
screen = pg.display.set_mode(size)

paintRect = LEFT_BOUND, 0, width-LEFT_BOUND, height # x,y,w,h
controlRect = 0, 0, LEFT_BOUND, height
paintScreen = screen.subsurface(paintRect)
controlScreen = screen.subsurface(controlRect)

pg.display.set_caption('Painter Plus')
paintScreen.fill((255,255,255))
controlScreen.fill(BG)


# draw colorTiles
for t in colorTiles:
    pg.draw.rect(controlScreen,t.getclr(),t.getrect())
    pg.draw.rect(controlScreen,(0,0,0),t.getrect(),1)


# draw slider method, with tick
def drawSlider(s,x,i=0):
    r = [s.getx(),s.gety()-2,s.getw(),s.geth()+4]
    pg.draw.rect(controlScreen,BG,r) # grey background

    # redraw slider
    if s.getrgb() != 3:
        l = [0,0]
        l.insert(s.getrgb(),255)
        pg.draw.rect(controlScreen,l,s.getrect())
    else:
        pg.draw.rect(controlScreen,(0,0,0),s.getrect(),1)

    # draw tick, update
    pg.draw.rect(controlScreen,(0,0,0),[x,s.gety()-2,2,s.geth()+4])
    pg.display.update(r)


# draw sliders
for s in sliders[:-1]:
    drawSlider(s,5)


def drawShape(n,r,c=(0,0,0)):

    pg.draw.rect(controlScreen,BG,r)

    x,y,w,h = r
    d = abs(w-h)
    w = min(w,h)

    if n==0:
        pg.draw.circle(controlScreen,c,[int(x+w/2.0+d/2.0),int(y+w/2.0)],int((w)/2.0))
    elif n==1:
        pg.draw.rect(controlScreen,c,[int(x+d/2.0),int(y),w,w])
    elif n==2:
        pg.draw.polygon(controlScreen,c,[[int(x + d/2.0),int(y+h-1)],[int(x + w + d/2.0),int(y+h-1)],[int(x + w/2.0 + d/2.0),int(y)]])
    elif n==3:
        pg.draw.line(controlScreen,c,[int(x + d/2.0),int(y)],[int(x + w + d/2.0),int(y+h)])

# draw shapeTiles
for n,s in enumerate(shapeTiles):
    drawShape(n,s.getrect())


def drawOutlineText(n,r,c=(0,0,0)):
    pg.draw.rect(controlScreen,BG,r)
    pg.draw.rect(controlScreen,(0,0,0),r,1)
    text = ['Fill','Outline']
    size = [32,13]
    screen.blit(pg.font.SysFont("monospace", 18).render(text[n], 1, c), (r[0]+size[n],r[1]+9))

# draw outlineTiles
for n,o in enumerate(outlineTiles):
    drawOutlineText(n,o.getrect())


def drawSpecialText(n,r,c=(0,0,0)):
    pg.draw.rect(controlScreen,BG,r)
    pg.draw.rect(controlScreen,(0,0,0),r,1)
    text = ['Fill','Redraw','Save']
    size = [14,7,15]
    screen.blit(pg.font.SysFont("monospace", 18 if text[n] !='Redraw' else 15).render(text[n], 1, c), (r[0]+size[n],r[1]+(10 if text[n] != 'Redraw' else 12)))

# draw specialTiles
for n,o in enumerate(specialTiles):
    drawSpecialText(n,o.getrect())


# start out with first of each highlighted
drawShape(0,shapeTiles[0].getrect(),HL)
drawOutlineText(0,outlineTiles[0].getrect(),HL)


# draw main color
colorRect = [5,colorHeight+PADDING+65,LEFT_BOUND-10,30]
currentColor = ColorTile((0,0,0),colorRect,False)
pg.draw.rect(controlScreen,currentColor.getclr(),currentColor.getrect())
pg.draw.rect(controlScreen,(0,0,0),[currentColor.getx()-1,currentColor.gety()-1,currentColor.getw()+2,currentColor.geth()+2],1)


# draw size section
drawSlider(sliders[-1],25)
pg.draw.circle(controlScreen,(0,0,0),[15,y+180],3,1)
pg.draw.circle(controlScreen,(0,0,0),[LEFT_BOUND-30,y+180],20,1)



pg.display.flip()

# ######################## SETUP DONE ######################## #


# lastPos,pos to test for movement of mouse
# other varss
lastPos = -1,-1
pos = lastPos
ableToPick,sliding,drawing,outline = True,[0,0,0,0],False,0
dragging,draggingCoords,draggingSurface = False,[0,0],None
lastDraw,drawings = [],[]
running = True

# main loop
while running:

    button = pg.mouse.get_pressed()

    # left button
    if 1 in button and 1 not in sliding:

        x,y = pg.mouse.get_pos()
        pos = x,y

        if (x >= LEFT_BOUND or drawing) and ableToPick:

            # check for mouse movement
            if lastPos != pos:

                lastPos = pos

                x -= LEFT_BOUND
                outline = 0 if outlineTiles[0].getIsSelected() else 1

                if not dragging:

                    click = button.index(1)
                    drawing = True

                    if x < 0:
                        x = 0

                    # dragging function
                    if click == 2 or shapeTiles[3].getIsSelected():

                        dragging = True
                        draggingCoords = x,y
                        draggingSurface = paintScreen.copy()

                    # regular drawing
                    elif click == 0:

                        # circle
                        if shapeTiles[0].getIsSelected():
                            pg.draw.circle(paintScreen, currentColor.getclr(), (x,y), SIZE,outline)
                            drawings.append([0,x,y,SIZE,SIZE,outline,currentColor.getclr()])

                        # square
                        elif shapeTiles[1].getIsSelected():
                            pg.draw.rect(paintScreen,currentColor.getclr(),[x-SIZE,y-SIZE,SIZE*2.0,SIZE*2.0],outline)
                            drawings.append([1,x,y,SIZE,SIZE,outline,currentColor.getclr()])

                        # triangle
                        elif shapeTiles[2].getIsSelected():
                            pg.draw.polygon(paintScreen,currentColor.getclr(),[[x,y-SIZE],[x-SIZE,y+SIZE],[x+SIZE,y+SIZE]],outline)
                            drawings.append([2,x,y,SIZE,SIZE,outline,currentColor.getclr()])

                        pg.display.update(paintRect)

                    else:

                        print('who uses a middle click?')

                # if dragging
                else:

                    paintScreen.blit(draggingSurface,[0,0])

                    # line
                    if shapeTiles[3].getIsSelected():
                        pg.draw.line(paintScreen,currentColor.getclr(),draggingCoords,[x,y],SIZE if not outline else 1)
                        lastDraw = [3,draggingCoords[0],draggingCoords[1],x,y,SIZE if not outline else 1,currentColor.getclr()]

                    # shape
                    else:
                        xd,yd = draggingCoords
                        dx,dy = x-xd,y-yd
                        if shapeTiles[0].getIsSelected():
                            r = [xd,yd,dx,dy]
                            if dx < 0:
                                r[0] = x
                                r[2] = -dx
                            if dy < 0:
                                r[1] = y
                                r[3] = -dy
                            if r[2] > 1 and r[3] > 1:
                                pg.draw.ellipse(paintScreen,currentColor.getclr(),r,outline)
                            lastDraw = [4,r[0],r[1],r[2],r[3],outline,currentColor.getclr()]
                        elif shapeTiles[1].getIsSelected():
                            pg.draw.rect(paintScreen,currentColor.getclr(),[xd,yd,dx,dy],outline)
                            lastDraw = [5,xd,yd,dx,dy,outline,currentColor.getclr()]
                        elif shapeTiles[2].getIsSelected():
                            pg.draw.polygon(paintScreen,currentColor.getclr(),[draggingCoords,[xd+dx,yd],[xd+dx/2.0,y]],outline)
                            lastDraw = [6,xd,yd,x,y,outline,currentColor.getclr()]

                    pg.display.update(paintRect)


        # PANEL CLICKS
        else:
            if ableToPick and button[0]:

                ableToPick = False

                # cycle through all objects
                for o in colorTiles + shapeTiles + outlineTiles + specialTiles + sliders:

                    # if it's selected
                    if o.clicked(x,y):

                        lastPos = pos

                        drawing = False

                        if 'tile' in o.type():

                            # color tiles
                            if 'color' in o.type():

                                # change color tile
                                currentColor.setclr((o.getclr()))
                                pg.draw.rect(controlScreen,currentColor.getclr(),currentColor.getrect())
                                pg.display.update(colorRect)

                                # update slider colorTiles to reflect newly chosen color
                                for n,s in enumerate(sliders):
                                    if n < 3:
                                        s.slide(currentColor.getclr()[n])
                                        xcoord = 5 + (currentColor.getclr()[n]*((LEFT_BOUND-12)/255.0))
                                        drawSlider(s,xcoord)
                                        pg.display.update(s.getrect())

                            # shape tiles
                            elif 'shape' in o.type():
                                o.selected(True)
                                drawShape(shapeTiles.index(o),o.getrect(),HL)
                                for i in range(len(shapeTiles)):
                                    if not shapeTiles[i].clicked(x,y):
                                        shapeTiles[i].selected(False)
                                        drawShape(i,shapeTiles[i].getrect())
                                pg.display.update(controlRect)

                            # outline tiles
                            elif 'outline' in o.type():
                                o.selected(True)
                                drawOutlineText(outlineTiles.index(o),o.getrect(),HL)
                                for i in range(len(outlineTiles)):
                                    if not outlineTiles[i].clicked(x,y):
                                        outlineTiles[i].selected(False)
                                        drawOutlineText(i,outlineTiles[i].getrect())
                                pg.display.update(controlRect)

                            # special action
                            elif 'special' in o.type():
                                o.selected(True)
                                drawSpecialText(specialTiles.index(o),o.getrect(),HL)
                                pg.display.update(controlRect)

                                n = specialTiles.index(o)

                                # fill
                                if n == 0:

                                    paintScreen.fill(currentColor.getclr())
                                    pg.display.update(paintRect)

                                    drawings = []

                                # redraw
                                elif n == 1:

                                    paintScreen.fill(randCol())
                                    newCols = {}

                                    # create newCols dict, one random color per color used
                                    for d in drawings:
                                        if d[6] not in newCols:
                                            newCols[d[6]] = randCol()

                                    # mode,x,y,w,h,outline,clr
                                    for d in drawings:
                                        if d[0] == 0:
                                            pg.draw.circle(paintScreen,newCols[d[6]], (d[1],d[2]), d[3],d[5])
                                        elif d[0] == 1:
                                            pg.draw.rect(paintScreen,newCols[d[6]],[d[1]-d[3],d[2]-d[3],d[3]*2.0,d[3]*2.0],d[5])
                                        elif d[0] == 2:
                                            pg.draw.polygon(paintScreen,newCols[d[6]],[[d[1],d[2]-d[3]],[d[1]-d[3],d[2]+d[3]],[d[1]+d[3],d[2]+d[3]]],d[5])
                                        elif d[0] == 3:
                                            pg.draw.line(paintScreen,newCols[d[6]],[d[1],d[2]],[d[3],d[4]],d[5])
                                        elif d[0] == 4:
                                            pg.draw.ellipse(paintScreen,newCols[d[6]],[d[1],d[2],d[3],d[4]],d[5])
                                        elif d[0] == 5:
                                            pg.draw.rect(paintScreen,newCols[d[6]],[d[1],d[2],d[3],d[4]],d[5])
                                        elif d[0] == 6:
                                            pg.draw.polygon(paintScreen,newCols[d[6]],[[d[1],d[2]],[d[3],d[2]],[d[1]+(d[3]-d[1])/2.0,d[4]]],d[5])

                                        d[6] = newCols[d[6]]

                                    pg.display.update(paintRect)

                                elif n == 2:

                                    pg.image.save(paintScreen,dateStr() + '.jpg')



                        # sliders
                        elif 'slider' in o.type():
                            sliding[o.getrgb()] = 1
                            for i in range(len(sliding)):
                                if i != o.getrgb():
                                    sliding[i] = 0


    elif not button[0] and not ableToPick:
        ableToPick = True

    # EVENT HANDLING
    for ev in pg.event.get():

        # QUIT
        if (ev.type is KEYDOWN and (ev.key is K_ESCAPE or ev.key is K_q)) or ev.type is QUIT:
            running = False

        # immediately redraw special tiles
        if ev.type is MOUSEBUTTONUP and 1 in [o.getIsSelected() for o in specialTiles]:

            for n,o in enumerate(specialTiles):
                o.selected(False)
                drawSpecialText(n,o.getrect())

            pg.display.update(controlRect)


        # SLIDERS
        if (ev.type is MOUSEMOTION or MOUSEBUTTONDOWN) and 1 in sliding:

            percent = ((ev.pos[0]-5)/(LEFT_BOUND-10))

            if percent <= 0:
                percent=0.0
            elif percent >= 1:
                percent=1.0

            # slide selected slider over the correct amount
            s = sliders[sliding.index(1)]
            s.slide(255*percent)

            x = ev.pos[0]
            if x <= 5:
                x = 5
            elif x >= LEFT_BOUND-7:
                x = LEFT_BOUND-7

            # size slider
            if 'size' in s.type():

                pg.draw.rect(controlScreen,BG,sizeSlider.getrect())
                SIZE = int(80*percent)+1

            # color sliders
            else:

                # draw large tile
                currentColor.setclr((sliders[0].getslider(),sliders[1].getslider(),sliders[2].getslider()))
                pg.draw.rect(controlScreen,currentColor.getclr(),colorRect)
                pg.display.update(colorRect)

            # draw slider
            drawSlider(s,x)


        # RESET SLIDERS
        if ev.type is MOUSEBUTTONUP:
            drawing = dragging = False
            if lastDraw:
                drawings.append(lastDraw)
                lastDraw = []
            sliding = [0,0,0,0]

if 0:
    pg.image.save(paintScreen,dateStr() + '.jpg')
    pg.display.set_caption('Saving')
    pg.time.wait(250)

pg.quit()