from Tile import Tile

class OutlineTile(Tile):
    def __init__(self,rect,isSelected):
        Tile.__init__(self,rect,isSelected)
        self.t = 'outlinetile'

    def getIsSelected(self):
        return self.isSelected
    def selected(self,s):
        self.isSelected=s

    def type(self):
        return self.t

    def setType(self,s):
        self.t = s


    def __repr__(self):
        return '{} {} {} {}'.format(self.isSelected,self.x,self.y,self.h)