from Tile import Tile

class ShapeTile(Tile):

    SHAPES = ['circle','square','triangle','line']

    def __init__(self,shape,rect,isSelected):
        Tile.__init__(self,rect,isSelected)
        self.shape = self.SHAPES[shape]

    def getshape(self):
        return self.shape

    def type(self):
        return 'shapetile'

    def getIsSelected(self):
        return self.isSelected
    def selected(self,s):
        self.isSelected=s

    def __repr__(self):
        return 'shape:{}, x:{}, y:{}, w:{}, h:{}, selected:{}' \
            .format(self.shape,self.x,self.y,self.w,self.h,self.isSelected)