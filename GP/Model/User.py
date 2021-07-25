
class User(object):
    
     __user_id = 0
     #Constructor 
     def __init__(self,name,email,c_id,password,date):
         self.__name = name
         self.__email = email
         self.__company_ID = c_id
         self.__password = password
         self.__date = date
     
     def set_name(self,newname):
         self.__name = newname

     def get_name(self):
         return self.__name

     def set_userid(self,userid):
         self.__user_id = userid

     def get_userid(self):
         return self.__user_id

     def set_email(self,newemail):
         self.__email = newemail
     
     def get_email(self):
         return self.__email 
         
     def set_password(self,newpass):
         self.__password = newpass
         
     def get_password(self):
          return self.__password 

     def set_company_id(self,newc_id):
         self.__company_ID = newc_id
     
     def get_company_id(self):
         return  self.__company_ID 
              
     def set_date(self,newdate):
         self.__date = newdate
         
     def get_date(self):
         return  self.__date

         

         

         
         """ User_ID =0
     Name='ssasa'
     Email=''
     Company_ID=0
     Password=''
     Date ='' 
     """

