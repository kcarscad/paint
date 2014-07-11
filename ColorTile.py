from Tile import Tile

class ColorTile(Tile):

    # init
    def __init__(self,clr,rect,isSelected):
        Tile.__init__(self,rect,isSelected)
        self.clr=clr

    def getclr(self):
        return self.clr
    def setclr(self,clr):
        self.clr=clr

    def type(self):
        return 'colortile'

    def __repr__(self):
        return 'c:{}, x:{}, y:{}, w:{}, h:{}, selected:{}' \
            .format(self.clr,self.x,self.y,self.w,self.h,self.isSelected)
