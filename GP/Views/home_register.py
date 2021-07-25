from flask import Flask,Blueprint,redirect,url_for,render_template,sessions,session
home = Blueprint('homereg',__name__)
import json
data_line={}
data_bar={}
data_pie={}
@home.route('/')
def main():
    with open('Accounts.json') as json_file:
       data = json.load(json_file)

    Accounts = (data['accounts']['data'])
    cols=['kora','akl', 'lbs']
    session['data_line']=data_line
    session['data_bar']=data_bar
    session['data_pie']=data_pie
   
    return render_template('graph chart.html',cols=cols,data_bar=data_bar,data_line=data_line,data_pie=data_pie)
    #return render_template('instgram page.html',Pages = Accounts)
    #return render_template('graph chart.html')


