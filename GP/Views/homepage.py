from flask import Flask,Blueprint,render_template
homepage = Blueprint('HomePage',__name__)


@homepage.route('/HomePage')
def main():
    #if "User_id" in session:
        #user = session["User_id"]
    return render_template("personal.html")



