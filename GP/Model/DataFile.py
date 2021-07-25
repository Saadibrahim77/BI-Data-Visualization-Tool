class DataFile(object):
  
    def __init__(self,ID, fileid, userid, reportid, date, platform, metrics):
        self.__ID = ID
        self.__fileid = fileid
        self.__user_id = userid
        self.__report_id = reportid
        self.__created_date = date
        self.__platform = platform
        self.__metrics = metrics
       
    def set_File_id(self ,id):
        self.__fileid=id

    def get_File_id(self):
        return self.__fileid
    
    def set_user_id(self ,id):
        self.__user_id =id

    def get_user_id(self):
        return self.__user_id
    
    def set_report_id(self,id):
        self.__report_id =id

    def get_report_id(self):
        return self.__report_id

    def set_date(self,date):
        self.__created_date = date
    
    def get_date(self):
        return self.__created_date

    def set_metrics(self ,metrics):
        self.__metrics = metrics

    def get_metrics(self):
        return self.__metrics

    def set_ID(self ,ID):
        self.__ID = ID

    def get_ID(self):
        return self.__ID

    
    def set_platform(self ,platform):
        self.__platform = platform

    def get_platform(self):
        return self.__platform
   
 




