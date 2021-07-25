from flask import Flask,Blueprint,render_template,request,url_for,redirect,session
import sqlite3
import threading
import os
import requests
import json
import urllib
import urllib3
import tkinter 

from  tkinter  import filedialog
import pandas as pd 
from pandas import json_normalize
from Views.home_register import home
from Views.login import loginpage
from Views.register import reg
from Views.homepage import homepage
from Views.ViewPages import page
from Views.ViewGraphs import graph
from Views.ExtractData import Platform
from Views.Report import PreviousRepo
from RepositoryFile.MyQuery import MyQuery
from RepositoryFile.MongoDB import MongoDB
from RepositoryFile.MyQuery import MyQuery
from Data.InstagramWR import InstagramWR
app = Flask(__name__)
app.config.from_object('Config')
app.config['SECRET_KEY']='sure'
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.register_blueprint(home)
app.register_blueprint(Platform,url_prefix='/platform')
app.register_blueprint(graph,url_prefix='/graph')
app.register_blueprint(page ,url_prefix='/page')
app.register_blueprint(homepage,url_prefix='/homepage')

app.register_blueprint(loginpage,url_prefix='/login')
app.register_blueprint(reg,url_prefix='/register')
app.register_blueprint(PreviousRepo,url_prefix='/Report')
wsgi_app = app.wsgi_app
        


@app.route('/profile/')
def my_profile():
    myquery=MyQuery()
    id=session['userid']
    text=myquery.getname(id)
    return render_template("view_personal.html",text=text)


@app.route('/DataSource')
def datasource():
    return render_template("data.html")


@app.route('/previousReport')
def previousReport():
    return render_template("reportinfo.html")





if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)