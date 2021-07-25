class Company(object):
    
    __company_id = 0
    def __init__(self,companyname,industry,date):
        self.__company_name = companyname
        self.__industry = industry
        self.__created_date=date
        
    #setter
    def set_company_name(self,name):
        self.__company_name = name
    
    def set_company_id(self,id):
        self. __company_id = id

    def set_industry(self,inst):
        self.__industry =inst 
        
    def set_date(self,date):
        self.__created_date= date

     #getter
    def get_company_name(self):
        return self.__company_name

    def get_industry(self):
        return self.__industry

    def get_date(self):
        return self.__created_date
    