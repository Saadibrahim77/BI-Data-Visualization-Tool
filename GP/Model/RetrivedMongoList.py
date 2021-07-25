class RetrivedMongoList(object):

    listvalues = []
    visual_id = -1 
    def __init__(self,listvalues, visual_id):
        self.listvalues = listvalues
        self.visual_id = visual_id

    def getspecificlists(self):
        return self.listvalues

    def getvisualid(self):
        return self.visual_id

    def setspecificlists(self,listvalues):
        self.list = listvalues

    def setvisualid(self,V_ID):
        self.visual_id = V_ID


