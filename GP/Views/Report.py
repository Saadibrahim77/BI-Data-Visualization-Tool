from flask import Flask,Blueprint,render_template , session
from Data.InstagramWR import InstagramWR
from Model.DataFile import DataFile
from RepositoryFile.MyQuery import MyQuery
from RepositoryFile.MongoDB import MongoDB
from Model.RetrivedMongoList import RetrivedMongoList
from Model.DataFile import DataFile
import pandas as pd
import json

PreviousRepo = Blueprint('PreviousReport',__name__)
@PreviousRepo.route('/')
def main():

   preReports = GetReports()
   return render_template("reportinfo.html",reports = preReports)

    


@PreviousRepo.route('/SelectedReport/<int:ReportID>')
def SelectedReport(ReportID:int):
    print(ReportID)
    q =MyQuery()
    platform_name = q.Retrieve_PlatformnameByreportid(ReportID)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(platform_name)
    
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    RetreivedVisuals = Load_Report(ReportID)
    for item in RetreivedVisuals:
        print(item.getvisualid())
        print("XXXXXXXXXXX")
        lts =  item.getspecificlists()
        for i in range(len(lts[0])):
            print(lts[0][i])
        print("YYYYYYYYYYYYYYYYYY")
        for i in range(len(lts[1])):
            print(lts[1][i])
    Jsonlist = json.dumps([ob.__dict__ for ob in RetreivedVisuals]) 
    
    if platform_name=="insta":
         return render_template("ShowReportInstagram.html",jsonlist = Jsonlist)
    else:
         return render_template("ShowReportLinkedIn.html",jsonlist = Jsonlist)

def GetReports():

    UserReports = list()
    queryInstance = MyQuery()
    userid = session['userid']
    UserReports = queryInstance.getReports(userid)
    return UserReports


def MongoToLists(file:DataFile):
    mongodb = MongoDB('abdullah', 'AbdullahEnayet')
    fileid = file.get_File_id()
    print(fileid)
    platform = file.get_platform()
    print(platform)
    metrics = file.get_metrics()
    print(metrics)
    metrics_list = metrics.split(',')
    #session['userid']
    df = mongodb.Get_JSON(platform,str(session['userid']), fileid)
    metric1 = df[metrics_list[0]].to_list()
    metric2 = df[metrics_list[1]].to_list()    
    return metric1, metric2

def Load_Report(report_id):
    retirved_visuals = list()
    
    QueryInstance = MyQuery()
    datafiles = QueryInstance.GetAll_datafiles(report_id)
    for file in datafiles:
        visual_id = QueryInstance.get_visualid(file.get_ID(), file.get_report_id())
        list1, list2 = MongoToLists(file)
        print("Lists!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(list1)
        print(list2)
        final_list = list()
        final_list.append(list1)
        final_list.append(list2)
        visual = RetrivedMongoList(final_list,visual_id)
        retirved_visuals.append(visual)
    return retirved_visuals
