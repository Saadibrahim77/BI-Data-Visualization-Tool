class Report(object):
     
    __report_id= 0
    def __init__(self,userid,date):
        self.__user_id = userid
        self.__created_date= date

    def get_user_id(self):
        return self.__user_id

    def set_date(self,date):
        self.__created_date= date
    
    def get_date(self):
        return self.__created_date