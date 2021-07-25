from flask import Flask,Blueprint,redirect,render_template,session,url_for
from Data.InstagramWR import InstagramWR
page = Blueprint('Page',__name__)
data_line={}
data_bar={}
data_pie={}
@page.route('/<string:pageid>/<string:pagename>')
def main(pageid,pagename):
    print(pagename + "->>>>>>>>>>>>>>")
    #print(session["Page_ID"])
    session["pagename"] = pagename
    if session["Platform"] == "insta":
        session["Page_ID"] = pageid[8:25]
        return redirect(url_for('Graph.Instagram_Data'))
    else:
        session["Page_ID"] = pageid
        return redirect(url_for('Graph.LinkedIn_Data'))
    


    #print(session["Page_ID"] )
    #insta = InstagramWR(session["Access_token"],session["Page_ID"])
    #return redirect(url_for('Graph.main'))
    
