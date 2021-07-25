class Report(object):
     
    __report_id = 0
    __user_id = 0
    def __init__(self,reportid,date,pagename):
        self.__report_id = reportid
        self.__created_date= date
        self.__pagename= pagename



    def set_user_id(self ,UID):
         self.__user_id = UID

    def get_user_id(self):
        return self.__user_id

    def set_report_id(self,RID):
         self.__user_id  =RID

    def get_Report_id(self):
        return self.__report_id


    def set_date(self,date):
        self.__created_date= date
    
    def get_date(self):
        return self.__created_date

    def set_pagename(self,pname):
         self.__pagename= pname
    
    def get_pagename(self):
        return self.__pagename