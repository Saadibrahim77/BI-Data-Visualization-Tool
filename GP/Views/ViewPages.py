from flask import Flask,Blueprint,redirect,render_template,url_for

page = Blueprint('Page',__name__)


@page.route('/<string:pageid>')
def main(pageid):
    return pageid

