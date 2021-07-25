class Organization(object):
        
    def __init__(self,name,ID,imageurl):
        self.name= name
        self.ID = ID
        self.Iurl = imageurl



    def GetOrganizationName(self):
        return self.name
 
    def GetOrganizationImageUrl(self):
        return self.Iurl

    def GetOrganizationTarget(self):
        return self.ID
 

    def SetOrganizationName(self,name):
         self.name = name
 
    def SetOrganizationImageUrl(self,Url):
         self.Iurl = Url

    def SetOrganizationTarget(self,ID):
        self.ID = ID
 

    
