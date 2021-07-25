import sqlite3
from datetime import datetime
from Model.Report import Report
from Model.DataFile import DataFile
class MyQuery():
    conn=None
    cursor = None
    
    def __init__(self):
      self.conn = sqlite3.connect('SureAnalytics.db')
      self.cursor=self.conn.cursor()

    def get_visualid(self, fileid, reportid):
        row = self.cursor.execute('SELECT visual_id FROM Units WHERE datafile_id=? and report_id=?',(fileid,reportid))
        row = row.fetchone()
        return row[0]

    def getname(self,id):
        row = self.cursor.execute('SELECT * FROM User WHERE user_id=?',(id,))
        row = row.fetchone()
        return row[1]

    def checkemail(self,email):
        row = self.cursor.execute('SELECT * FROM User WHERE email=?',(email,))
        row = row.fetchone()
        if row==None:
            #self.conn.close()
            return False
        else:
            #self.conn.close()
            return True

    def UpdatePasswordBYEmail(self,email,Npassword):
        self.cursor.execute("update User set password = ? where email = ? " , (Npassword,email)) 
        self.conn.commit()

    def checkemailandpassword(self,email,password):
        row=self.cursor.execute('SELECT * FROM User WHERE email=? AND password=?',(email,password))
        row=row.fetchone()
        if row==None:
            #self.conn.close()
            return False
        else:
            #self.conn.close()
            return True
     
    def SetCompany(self,name,industry):
        self.cursor.execute("Insert into Company (company_name,industry) values(?,?)",(name,industry))
        self.conn.commit()
        return True

    def SetReport(self, user_id,created_date,pagename):
        
        self.cursor.execute("Insert into Report (user_id,created_date,page_name) values(?,?,?)",(user_id,created_date,pagename))
        self.conn.commit()
        self.cursor.execute("SELECT report_id FROM Report WHERE user_id =? and created_date = ?",(user_id,created_date))
        row = self.cursor.fetchone()
        return row[0]
    
    def getReports(self,UID):
         self.cursor.execute('SELECT * FROM Report WHERE user_id =?',(UID,))
         user_reports = list()
         rows =  self.cursor.fetchall()
         for row in rows:
            report_inst =  Report(row[0],row[2],row[3])
            user_reports.append(report_inst)
         return user_reports


    def SetUnit(self, visual_id, datafile_id, report_id):
        self.cursor.execute("Insert into Units (visual_id, datafile_id, report_id) values(?,?,?)",(visual_id,datafile_id,report_id))
        self.conn.commit()
        print("Unit DETAILS SAVED TO SQLITE DATABASE! ")
        return True
                              
    def GetCompanyID(self,name,industry):
        row = self.cursor.execute('SELECT * FROM Company WHERE company_name =? and industry=? ',(name,industry,))
        row=row.fetchone()
        if row!=None:   
            index=row[0]
            return index
        else:
            return None

    def getuserid(self,email,password):
        row=self.cursor.execute('SELECT * FROM User WHERE email=? AND password=?',(email,password))
        row=row.fetchone()
        if row==None:
            
            return False
        else:
            return row[0]
              
    def InsertUser(self, name, email, password, C_ID, date):
         self.cursor.execute("INSERT INTO User (name,email,password,company_ID,created_date) VALUES (?,?,?,?,?)",(name,email,password,C_ID,date) )
         self.conn.commit()
         print("NEW USER SAVED TO SQLITE DATABASE! ")
         return True 

    def Save_DataFile(self, datafile_id, user_id, report_id, platform_name,date,metrics):
        query = "INSERT into DataFile (File_ID, user_id, report_id, created_date, platform_name,metric_name) VALUES (?,?,?,?,?,?)"
       
        self.cursor.execute(query,(datafile_id, user_id, report_id, date, platform_name,metrics))
        self.conn.commit()
        self.cursor.execute("select ID from DataFile where created_date = ? ",(date,))
        row = self.cursor.fetchone()
        print("DATAFILE DETAILS SAVED TO SQLITE DATABASE! ")
        return row[0]

    def GetAll_datafiles(self, report_id):
        self.cursor.execute('SELECT * FROM DataFile WHERE report_id =?',(report_id,))
        rep_datafiles = list()
        rows =  self.cursor.fetchall()
        for row in rows:
            file_inst = DataFile(row[0],row[6], row[1], row[2], row[3], row[4], row[5])
            rep_datafiles.append(file_inst)
            
        return rep_datafiles

    def Retrieve_PlatformnameByreportid(self, report_id):
        query = 'SELECT platform_name FROM DataFile WHERE report_id =?'
        self.cursor.execute(query,(report_id,))
        result = self.cursor.fetchone()
        return result[0]
    
    def CloseConnection(self):
        self.conn.close()
         


   

