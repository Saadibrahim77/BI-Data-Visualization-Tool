import sqlite3
class MyQuery():
    conn=None
    cursor = None
    
    def __init__(self):
      self.conn = sqlite3.connect('SureAnalytics.db')
      self.cursor=self.conn.cursor()
    def getname(self,id):

        row=self.cursor.execute('SELECT * FROM User WHERE user_id=?',(id,))
        row=row.fetchone()
        return row[1]

    def checkemail(self,email):
        row=self.cursor.execute('SELECT * FROM User WHERE email=?',(email,))
        row=row.fetchone()
        if row==None:
            #self.conn.close()
            return False
        else:
            #self.conn.close()
            return True

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
              
                 #cursor.execute("INSERT INTO User (name,email,password,company_ID,created_date)  VALUES (?,?,?,?,?)",(username,email,password,index,date) )
                
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
            
           
    def InsertUser(self,name,email,password,C_ID,date):
         self.cursor.execute("INSERT INTO User (name,email,password,company_ID,created_date) VALUES (?,?,?,?,?)",(name,email,password,C_ID,date) )
         self.conn.commit()


    def Save_DataFile(self, datafile_id, user_id, report_id, created_date):
        #insert into datafile (....) values (....)
        print("DATAFILE DETAILS SAVED TO SQLITE DATABASE! ")


    def Retrieve_DataFile(self):
        #select datafile_id where user_id = X and report_id = Y
        datafile_id = 0
        return datafile_id
    

    
    def CloseConnection(self):
        self.conn.close()
         


   

