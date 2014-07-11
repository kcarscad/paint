class Slider(object):

    # coords(x,y), int (0-2)
    def __init__(self,x,y,w,h,rgb):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.rgb=rgb
        self.slider=0

    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getw(self):
        return self.w
    def geth(self):
        return self.h
    def getrgb(self):
        return self.rgb
    def getslider(self):
        return self.slider

    def getrect(self):
        return [self.x,self.y,self.w,self.h]

    def slide(self,x):
        self.slider = x

        if self.slider >= 255:
            self.slider = 255
        if self.slider <= 0:
            self.slider = 0

        return self.slider

    def clicked(self,x,y):
        clicked=False
        if self.x <= x <= self.x+self.w and self.y <= y <= self.y+self.h:
            clicked=True
        return clicked

    def type(self):
        if self.rgb == 3:
            return 'slidersize'
        else:
            return 'slidercolor'

    def __repr__(self):
        return 'x:{} y:{} w:{} rgb:{} slider:{}'.format(self.x,self.y,self.w,('r','g','b')[self.rgb],self.slider)