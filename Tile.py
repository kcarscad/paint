class Tile(object):

    def __init__(self,rect,isSelected):
        self.x=rect[0]
        self.y=rect[1]
        self.w=rect[2]
        self.h=rect[3]
        self.isSelected=isSelected

    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getw(self):
        return self.w
    def geth(self):
        return self.h

    def getrect(self):
        return [self.x,self.y,self.w,self.h]

    def clicked(self,x,y):
        if self.x <= x <= self.x+self.w and self.y <= y <= self.y+self.h:
            return True
        return False

    def __repr__(self):
    	return 'x:{} y:{} w:{} h:{} isSelected:{}'.format(self.x,self.y,self.w,self.h,self.isSelected)
