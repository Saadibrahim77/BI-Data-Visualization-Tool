from flask import Flask ,Blueprint,url_for,redirect,render_template,request,session
import sqlite3
#from Model import User,Company
from RepositoryFile.MyQuery import MyQuery

loginpage = Blueprint('Login',__name__)


@loginpage.route('/')
def main():
    return render_template('login.html')


@loginpage.route('/login_action',methods=['POST','get'])
def LoginAction():
    error=None
    email=request.form['email']
    password=request.form['password']
    myquery = MyQuery()
    check = myquery.checkemailandpassword(email,password)
    if(check==True):
        session['userid']=myquery.getuserid(email,password)
        return redirect(url_for('HomePage.main'))
    else:
        error = 'Invalid Credentials. Please try again.'
        return error
      


