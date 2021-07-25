from flask import Blueprint,request,redirect,render_template,session,sessions
graph = Blueprint("Graph",__name__)
from Data.InstagramWR import InstagramWR
from Data.LinkedIn import LinkedIn
from Model.DataFile import DataFile
from RepositoryFile.MyQuery import MyQuery
from RepositoryFile.MongoDB import MongoDB
from Model.RetrivedMongoList import RetrivedMongoList
from Model.DataFile import DataFile
from Model.ValueOfFile import ValueOfFile
import numpy as np
import pandas as pd
import json
from datetime import datetime

HeadersOfFiles= list()
RetrievedObjectsJS= list()
GraphIndex = list()




@graph.route("/InstagramData")
def Instagram_Data():
    insta = InstagramWR(session["Access_token"], session["Page_ID"]) 
    insta.Extract_Data()
    # Get Columns name form each json document
    GetValuesFromJson(insta)
    #Save_Data_Mongo(insta)
    LanguagesList, FollowersbyLanguage = insta.generate_Languages_Lists()
    citiesList,FollowersbyCity = insta.generate_City_Lists()
    
    countriesList,FollowersbyCountry = insta.generate_Countries_Lists()
    ProfileViewlist, impressionslist, reachlist, DayOfWeeklist, l1, l2, l3, maximp, maxprofile, maxreach, insights = insta.generate_Days_Lists()
    df=insights
    return render_template('Instagram_Graphs.html',LanguagesList=LanguagesList
                           ,FollowersbyLanguage=FollowersbyLanguage
                           ,countriesList=countriesList
                           ,FollowersbyCountry=FollowersbyCountry
                           ,citiesList=citiesList,FollowersbyCity=FollowersbyCity
                           ,DayOfWeeklist=DayOfWeeklist
                           ,ProfileViewlist=ProfileViewlist
                           ,impressionslist=impressionslist
                           ,reachlist=reachlist
                           ,maximp=maximp,maxprofile=maxprofile,maxreach=maxreach
                           ,column_names=df.columns.values
                           ,row_data=list(df.values.tolist()) #  
                           ,link_column="Patient ID", zip=zip,
                           jsonlist = json.dumps([ob.__dict__ for ob in HeadersOfFiles]))


 
def GetValuesFromJson(platforminstance):
    mongodb = MongoDB('abdullah', 'AbdullahEnayet')        
        
    if session["Platform"] == "insta":
        countries = platforminstance.generate_Countries_Json()
        cites = platforminstance.generate_City_Json()
        days = platforminstance.generate_Days_Json()
        followers = platforminstance.generate_followers_Json()
        languages = platforminstance.generate_Languages_Json()
        Documentlistinsta = [countries,cites,days,followers,languages]
        for item in Documentlistinsta:
            jsonfile = json.dumps(item)
            jsonfile = json.loads(jsonfile)
            #str(session['userid'])
            fileid = mongodb.Push_JSON(session["Platform"],str(session['userid']),item)
            headers = list()    
            for key in jsonfile.keys():
                #print(key)
                headers.append(key)

            print("!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            obj = ValueOfFile(fileid,headers)
            HeadersOfFiles.append(obj)
    else:

        fassocciation = platforminstance.Generate_FollowersbyAssocciation_Json() 
        days = platforminstance.Generate_30days_shares_Json()
        countries = platforminstance.Generate_FollowersbyCountries_Json()
        functions = platforminstance.Generate_FollowersbyFunctions_Json()
        industries = platforminstance.Generate_FollowersbyIndustries_Json()
        seniorities = platforminstance.Generate_FollowersbySeniorities_Json()
        staff =  platforminstance.Generate_FollowersbyStaff_Json()
        Documentlistin = [fassocciation,countries,days,functions,industries,seniorities,staff]
        for item in Documentlistin:
            jsonfile = json.dumps(item)
            #print(jsonfile)
            jsonfile = json.loads(jsonfile)
            #str(session['userid'])
            fileid = mongodb.Push_JSON(session["Platform"],str(session['userid']),item)
            headers = list()    
            for key in jsonfile.keys():
                print(key)
                headers.append(key)

               

            obj = ValueOfFile(fileid,headers)
            HeadersOfFiles.append(obj)
            print("!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")  
            
@graph.route("/SaveReport")
def SaveReport():
    QueryInstance = MyQuery()
    print("!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Report")
    created_date = str(datetime.now())
    created_date = created_date[0:16]
 
    report_id =  QueryInstance.SetReport(session['userid'],created_date,session["pagename"])
    if RetrievedObjectsJS.count!=0:
      
          for i in range(len(RetrievedObjectsJS)):
                filecreated_date = str(datetime.now())
                metric = str(RetrievedObjectsJS[i].values[0])+","+str(RetrievedObjectsJS[i].values[1])
    
                f_id =  QueryInstance.Save_DataFile(RetrievedObjectsJS[i].file_id
                                            ,session['userid'],report_id,
                                            session["Platform"]
                                            ,filecreated_date,metric)
    
                QueryInstance.SetUnit(GraphIndex[i],f_id,report_id)
    
          print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
          RetrievedObjectsJS.clear()
          GraphIndex.clear()
          HeadersOfFiles.clear()
    else:
        print("No Values for report")
    return  '', 204

  
@graph.route("/PieMetrics",methods=["POST"])
def Piemetrics():
    print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>GraphPie")
    req = request.data
    print(str(req))
    j = json.loads(req)
    u = ValueOfFile(**j)
    print(str(u.values))
    print(u.file_id)
    RetrievedObjectsJS.append(u)
    GraphIndex.append(3)
    
    return  '', 204

@graph.route("/BarMetrics",methods=["POST"])
def Barmetrics():
    print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>GraphBar")
    req = request.data
    print(str(req))
    j = json.loads(req)
    u = ValueOfFile(**j)
    print(u.file_id)
    print(u.values)
    RetrievedObjectsJS.append(u)
    GraphIndex.append(1)
    return  '', 204


@graph.route("/LineMetrics",methods=["POST"])
def Linemetrics():
    print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>GraphLine")
    req = request.data
    print(str(req))
    j = json.loads(req)
    u = ValueOfFile(**j)
    print(u.file_id)
    print(u.values)
    RetrievedObjectsJS.append(u)
    GraphIndex.append(2)
    return  '', 204


@graph.route("/ScatterMetrics",methods=["POST"])
def scattermetrics():
    print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>GraphScaa")
    req = request.data
    print(str(req))
    j = json.loads(req)
    u = ValueOfFile(**j)
    print(u.file_id)
    print(u.values)
    RetrievedObjectsJS.append(u)
    GraphIndex.append(4)
    return  '', 204

    


@graph.route("/Metrics",methods=["POST"])
def metrics():
    item = request.form["barxoptions"]
    SelectedItems.append(item)
    for i in SelectedItems:
        print(i)
    #print(item)
    return  '', 204




@graph.route("/LinkedInData")
def LinkedIn_Data():

    linkedin = LinkedIn(session["Access_token"],session["Page_ID"])
    linkedin.Extract_Data()
    GetValuesFromJson(linkedin)
    #Go to Graph With data from Linkedin  
    df = linkedin.Shares_Statistics_30Days
    countriesList,FollowersbyCountry=linkedin.Generate_FollowersbyCountries_Lists()
    #citiesList,FollowersbyCity
    SeniorityList,FollowersbySeniority=linkedin.Generate_FollowersbySeniorities_List()
    StaffList,FollowersbyStaff=linkedin.Generate_FollowersbyStaff_Lists()
    IndustriesList,FollowersbyIndustry=linkedin.Generate_FollowersbyIndustries_Lists()
    AssociationList,FollowersbyAssociation=linkedin.Generate_FollowersbyAssocciation_Lists()
    FunctionsList,FollowersbyFunction=linkedin.Generate_FollowersbyFunctions_Lists()
    Day, Month, Year, ImpressionsCount, Engagement, ShareCount, LikeCount, maximp, maxEngagement, maxShareCount, maxLikeCount = linkedin.Generate_30days_shares_Lists()
   

    return render_template('Linkedin_Graphs.html'
                           ,countriesList=countriesList
                           ,FollowersbyCountry=FollowersbyCountry
                           ,SeniorityList=SeniorityList
                           ,FollowersbySeniority=FollowersbySeniority
                           ,StaffList=StaffList,FollowersbyStaff=FollowersbyStaff
                           ,IndustriesList=IndustriesList,FollowersbyIndustry=FollowersbyIndustry
                           ,AssociationList=AssociationList,
                            FollowersbyAssociation=FollowersbyAssociation,
                            FunctionsList=FunctionsList,FollowersbyFunction=FollowersbyFunction
                            ,Day=Day,Month=Month,Year=Year,
                            ImpressionsCount=ImpressionsCount,
                            Engagement=Engagement,ShareCount=ShareCount
                            ,LikeCount=LikeCount,maximp=maximp,maxEngagement=maxEngagement
                            ,maxShareCount=maxShareCount,maxLikeCount=maxLikeCount,
                            column_names=df.columns.values
                            , row_data=list(df.values.tolist()),
                            link_column="Patient ID", 
                            zip=zip,
                            jsonlist = json.dumps([ob.__dict__ for ob in HeadersOfFiles]))





@graph.route('/')
def main():
    pass
    
    



