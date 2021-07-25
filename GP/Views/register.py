from flask import Flask,Blueprint,request,render_template,redirect,url_for
import sqlite3
#from Model import User,Company
from RepositoryFile.MyQuery import MyQuery
reg = Blueprint('Reg',__name__)

conn=sqlite3.connect('SureAnalytics.db')
    
@reg.route('/')
def main():
    return render_template('register.html')


@reg.route('/register_action',methods=['POST'])
def register():

    fname = request.form['fname']
    lname = request.form['lname']
    name = fname+lname
    industry = request.form['industry']
    companyname=request.form['company_name']
    date=request.form['date']
    #username=request.form['user_name']
    email=request.form['email']
    password=request.form['password']
    myquery = MyQuery()
    ID = myquery.GetCompanyID(companyname,industry)
    
    if(ID!=None):
        if myquery.checkemail(email)==False:
             myquery.InsertUser(name,email,password,ID,date)
             return redirect(url_for('HomePage.main'))
        else:
            return "email used before"
    else:
        if myquery.checkemail(email)==False:
            myquery.SetCompany(companyname,industry)
            ID = myquery.GetCompanyID(companyname,industry)
            myquery.InsertUser(name,email,password,ID,date)
            return redirect(url_for('HomePage.main'))
        else:
            return"email used before"


