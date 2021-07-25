class DataFile(object):
       
    __file_id=0
    def __init__(self,userid,reportid,date):
        self.__user_id = userid
        self.__report_id = reportid
        self.__created_date = date
       


    def set_user_id(self ,id):
        self.__user_id =id

    def get_user_id(self):
        return __user_id
    
    def set_report_id(self,id):
        self.__report_id =id

    def get_report_id(self):
        return self.__report_id

    def set_date(self,date):
        self.__created_date = date
    
    def get_date(self):
        return self.__created_date

    
   
 




