from flask import Flask,Blueprint,redirect,url_for,render_template,sessions,session


home = Blueprint('homereg',__name__)
import json
data_line={}
data_bar={}
data_pie={}
@home.route('/')
def main():

    return render_template('home.html')
   # return render_template('WebPage1.html', lol = list1, lol1 = list2)


