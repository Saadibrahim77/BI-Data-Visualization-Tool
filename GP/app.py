from flask import Flask,Blueprint,render_template,request,url_for,redirect,session
import sqlite3
import os
import requests
import json
import urllib
import urllib3
from pandas import json_normalize
from Views.home_register import home
from Views.login import loginpage
from Views.register import reg
from Views.homepage import homepage
from Views.ViewPages import page
from Views.ViewGraphs import graph
from RepositoryFile.MyQuery import MyQuery
app = Flask(__name__)
app.config.from_object('Config')
app.config['SECRET_KEY']='sure'
app.register_blueprint(home)
app.register_blueprint(graph,url_prefix='/graph')
app.register_blueprint(page ,url_prefix='/page')
app.register_blueprint(homepage,url_prefix='/homepage')
app.register_blueprint(homepage,url_prefix='/Pages')
app.register_blueprint(loginpage,url_prefix='/login')
app.register_blueprint(reg,url_prefix='/register')
wsgi_app = app.wsgi_app
        
"""@app.route('/')
def SetPages():
    with open('Accounts.json') as json_file:
       data = json.load(json_file)

    Accounts = (data['accounts']['data'][0])
    return Accounts["name"]
    #render_template('')
"""


@app.route('/profile/')
def my_profile():
    myquery=MyQuery()
    id=session['userid']
    text=myquery.getname(id)
    return render_template("view_personal.html",text=text)


@app.route('/data')
def datasource():
    return render_template("data.html")

def GetPages(access_token):
    print(access_token)
    fields = "&fields=accounts{access_token,name,picture.type(large){url}, instagram_business_account}"
    url = "https://graph.facebook.com/me?access_token=" + access_token + fields
    #"https://api.thedogapi.com/v1/breeds"
    response = requests.get(url)
    Error = response.raise_for_status()
    
    #Accounts = (json_normalize(response.json()['accounts']['data']))
    return # str(Accounts)
    





@app.route('/Instagram/AccessToken/<string:access_token>')
def GetUserAccessToken(access_token):
    print(access_token)
    return GetPages(access_token)
    

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)
    app.run(port = app.config['PORT'],debug  =app.config['DEBUG'])
