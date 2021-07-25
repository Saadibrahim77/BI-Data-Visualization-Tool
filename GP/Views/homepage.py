from flask import Flask,Blueprint,render_template
homepage = Blueprint('HomePage',__name__)


@homepage.route('/')
def main():
    
    return render_template("personal.html")



