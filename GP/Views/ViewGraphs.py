from flask import Blueprint,request,redirect,render_template,session,sessions
graph = Blueprint("Graph",__name__)

@graph.route("\PieGraph",methods=['POST','get'])
def PieFunction():
    selectx = request.form.get('myoptionx')
    selecty=selectx = request.form.get('myoptionx')
    cols=['kora','akl', 'lbs']
    data_pie={"barce":12,"real":15,"bayer":30}
   
    session['data_pie']=data_pie
    
   
    return render_template('graph chart.html',cols=cols,data_bar=session['data_bar'],data_line=session['data_line'],data_pie=session['data_pie'])


@graph.route("\BarGraph",methods=['POST','get'])
def BarFunction():
    selectx = request.form.get('myoptionx')
    selecty=selectx = request.form.get('myoptionx')
    cols=['kora','akl', 'lbs']
    data_bar={"barce":12,"real":15,"bayer":30}
    session['data_bar']=data_bar
    
    return render_template('graph chart.html',cols=cols,data_bar=session['data_bar'],data_line=session['data_line'],data_pie=session['data_pie'])
    
    



@graph.route("\LineGraph",methods=['POST','get'])
def LineFunction():
    selectx = request.form.get('myoptionx')
    selecty=selectx = request.form.get('myoptionx')
    cols=['kora','akl', 'lbs']
    data_line={"barce":12,"real":15,"bayer":30}
    session['data_line']=data_line
    return render_template('graph chart.html',cols=cols,data_bar=session['data_bar'],data_line=session['data_line'],data_pie=session['data_pie'])



@graph.route("\CardGraph",methods=['POST','get'])
def CardFunction():
    pass

