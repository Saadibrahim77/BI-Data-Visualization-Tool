class Unit(object):
      

    def __init__(self,x,y,graph_id):
        self.xlabel = x
        self.ylabel = y
        self.graphid = graph_id




    def setxlabel(self,x):
         self.xlabel = x
             
    def setylabel(self,y):
         self.ylabel = y

    def setgraphid(self,id):
         self.graphid = id


    def getxlabel(self):
        return self.xlabel 
             
    def getylabel(self):
        return self.ylabel 

    def getgraphid(self):
        return self.graphid 

