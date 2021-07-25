
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 21:11:50 2021

@author: Ahmed Refaat
"""

import pandas as pd
import numpy as np
from pandas import json_normalize
import requests
import sys 
import calendar
import time
import json 

class LinkedIn:
    Access_Token = None
    Organization_ID = None
    Lifetime_statistics = None 
    Organization_Statistics = None
    Followers_Statistics = None
    CountriesTable = None
    FunctionsTable = None
    SenioritiesTable = None
    IndustriesTable = None
    Total_Followers_Count = None
    Shares_Statistics_30Days = None
    def __init__(self, Access_Token, Organization_ID):
        self.Access_Token = Access_Token
        self.Organization_ID = Organization_ID
    
    def Extract_Data(self):
        Lifetime_statistics = 'https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity='+ self.Organization_ID
        Response = requests.get(Lifetime_statistics,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        Lifetime_statistics = Response.json()
        Lifetime_statistics = Lifetime_statistics['elements']
        Lifetime_statistics = json_normalize(Lifetime_statistics[0]['totalShareStatistics'])
        # Retrieved Lifetime_statistics
        
        
        Organization_Statistics='https://api.linkedin.com/v2/organizationPageStatistics?q=organization&organization='+ self.Organization_ID        
        Response = requests.get(Organization_Statistics,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        Organization_Statistics = Response.json()
        Organization_Statistics = Organization_Statistics['elements']
        Organization_Statistics = json_normalize(Organization_Statistics)
        # Retrived Organizational Statistics-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        End_Time = calendar.timegm(time.gmtime())
        Start_Time = End_Time - 2592000
        End_Time = End_Time *1000
        Start_Time = Start_Time *1000
        Shares_Statistics_30Days = 'https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity='+ self.Organization_ID +'&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start='+str(Start_Time)+'&timeIntervals.timeRange.end='+str(End_Time)
        Response = requests.get(Shares_Statistics_30Days,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        Shares_Statistics_30Days = Response.json()
        Shares_Statistics_30Days = Shares_Statistics_30Days['elements']
        Shares_Statistics_30Days = json_normalize(Shares_Statistics_30Days)
        #Retrieved 30 days Shares-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        Followers_Statistics ='https://api.linkedin.com/v2/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity='+ self.Organization_ID
        Response = requests.get(Followers_Statistics,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        Followers_Statistics = Response.json()
        Followers_Statistics = (Followers_Statistics['elements'])
        #this tabe is used to be merged with others so it is normalized when needed
        #Retrieved Followers Lifetime Statistics-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        
        CountriesTable = 'https://api.linkedin.com/v2/countries'
        Response = requests.get(CountriesTable,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        CountriesTable = Response.json()
        CountriesTable = json_normalize(CountriesTable['elements'])
        #THIS REQUEST SHPULD BE SAVED IN OUR FILES AS IT IS A CONSTANT REQUEST
        
        
        FunctionsTable = 'https://api.linkedin.com/v2/functions'
        Response = requests.get(FunctionsTable,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        FunctionsTable = Response.json()
        FunctionsTable = json_normalize(FunctionsTable['elements'])
        #THIS REQUEST SHPULD BE SAVED IN OUR FILES AS IT IS A CONSTANT REQUEST

        SenioritiesTable = 'https://api.linkedin.com/v2/seniorities'
        Response = requests.get(SenioritiesTable,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        SenioritiesTable = Response.json()
        SenioritiesTable = json_normalize(SenioritiesTable['elements'])
        #THIS REQUEST SHPULD BE SAVED IN OUR FILES AS IT IS A CONSTANT REQUEST
        
        IndustriesTable = 'https://api.linkedin.com/v2/industries'
        Response = requests.get(IndustriesTable,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        IndustriesTable = Response.json()
        IndustriesTable = json_normalize(IndustriesTable['elements'])
        #THIS REQUEST SHPULD BE SAVED IN OUR FILES AS IT IS A CONSTANT REQUEST
        
        Total_Followers_Count = 'https://api.linkedin.com/v2/networkSizes/' + self.Organization_ID+ '?edgeType=CompanyFollowedByMember'
        Response = requests.get(Total_Followers_Count,headers={"Authorization":"Bearer " + self.Access_Token})
        Response.raise_for_status()
        Total_Followers_Count = json_normalize(Response.json())
        
        self.Lifetime_statistics = Lifetime_statistics  
        self.Organization_Statistics = Organization_Statistics
        self.Followers_Statistics = Followers_Statistics
        self.CountriesTable = CountriesTable
        self.FunctionsTable = FunctionsTable
        self.SenioritiesTable = SenioritiesTable
        self.IndustriesTable = IndustriesTable
        self.Total_Followers_Count = Total_Followers_Count
        self.Shares_Statistics_30Days = Shares_Statistics_30Days
        return Lifetime_statistics, Organization_Statistics, Followers_Statistics, CountriesTable, FunctionsTable, SenioritiesTable, IndustriesTable, Total_Followers_Count, Shares_Statistics_30Days
     
    def Generate_Organization_Statistics(self):
        Organization_Statistics = self.Organization_Statistics.drop(['pageStatisticsBySeniority','pageStatisticsByCountry','pageStatisticsByIndustry',
                                        'pageStatisticsByStaffCountRange','pageStatisticsByRegion','pageStatisticsByFunction'],axis=1)
        return Organization_Statistics
    
    def Generate_FollowersbyCountries_Lists(self):
        CountriesTable = self.CountriesTable.drop(['name.locale.country','name.locale.language'],axis=1)
        CountriesFollowersTable = self.Followers_Statistics
        CountriesFollowersTable =json_normalize(CountriesFollowersTable[0]['followerCountsByCountry']) 
        Countries = pd.merge(CountriesTable,CountriesFollowersTable,right_on='country',left_on='$URN')
        Countries['total_followers'] = Countries['followerCounts.organicFollowerCount'] + Countries['followerCounts.paidFollowerCount']
        Countries = Countries.drop(['$URN', 'country', 'countryGroup', 'followerCounts.organicFollowerCount', 'followerCounts.paidFollowerCount'],axis=1)
        CountriesList = Countries['name.value'].tolist()
        FollowersList = Countries['total_followers'].tolist()
        return CountriesList, FollowersList

    def Generate_FollowersbyCountries_Json(self):
        CountriesTable = self.CountriesTable.drop(['name.locale.country','name.locale.language'],axis=1)
        CountriesFollowersTable = self.Followers_Statistics
        CountriesFollowersTable =json_normalize(CountriesFollowersTable[0]['followerCountsByCountry']) 
        Countries = pd.merge(CountriesTable,CountriesFollowersTable,right_on='country',left_on='$URN')
        Countries['total_followers'] = Countries['followerCounts.organicFollowerCount'] + Countries['followerCounts.paidFollowerCount']
        Countries = Countries.drop(['$URN', 'country', 'countryGroup', 'followerCounts.organicFollowerCount', 'followerCounts.paidFollowerCount'],axis=1)
        Countries = Countries.rename(columns = {"name.value":"country_name"})       
        Countries.index = Countries.index.map(str)
        Countries = Countries.to_dict()
        return Countries

    def Generate_FollowersbyFunctions_Lists(self):
        FunctionsTable=self.FunctionsTable
        FunctionsFollowersTable = self.Followers_Statistics
        FunctionsFollowersTable = json_normalize(FunctionsFollowersTable[0]['followerCountsByFunction']) 
        Functions = pd.merge(FunctionsTable,FunctionsFollowersTable,right_on='function',left_on='$URN')
        Functions['total_followers'] = Functions['followerCounts.organicFollowerCount'] + Functions['followerCounts.paidFollowerCount']
        Functions = Functions.drop(['$URN','id','function','followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        FunctionsList = Functions['name.localized.en_US'].tolist()
        FollowersList = Functions['total_followers'].tolist()
        return FunctionsList, FollowersList

    def Generate_FollowersbyFunctions_Json(self):
        FunctionsTable=self.FunctionsTable
        FunctionsFollowersTable = self.Followers_Statistics
        FunctionsFollowersTable = json_normalize(FunctionsFollowersTable[0]['followerCountsByFunction']) 
        Functions = pd.merge(FunctionsTable,FunctionsFollowersTable,right_on='function',left_on='$URN')
        Functions['total_followers'] = Functions['followerCounts.organicFollowerCount'] + Functions['followerCounts.paidFollowerCount']
        Functions = Functions.drop(['$URN','id','function','followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        Functions = Functions.rename(columns = {"name.localized.en_US":"functions_name"}) 
        Functions.index = Functions.index.map(str)
        Functions = Functions.to_dict()
        return Functions
    
    def Generate_FollowersbyIndustries_Lists(self):
        IndustriesTable=self.IndustriesTable
        IndustriesFollowersTable = self.Followers_Statistics
        IndustriesFollowersTable = json_normalize(IndustriesFollowersTable[0]['followerCountsByIndustry']) 
        Industries = pd.merge(IndustriesTable,IndustriesFollowersTable,right_on='industry',left_on='$URN')
        Industries['total_followers'] = Industries['followerCounts.organicFollowerCount'] + Industries['followerCounts.paidFollowerCount']
        Industries = Industries.drop(['$URN','id','industry','followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        IndustriesList = Industries['name.localized.en_US'].tolist()
        FollowersList = Industries['total_followers'].tolist()
        return IndustriesList, FollowersList

    def Generate_FollowersbyIndustries_Json(self):
        IndustriesTable=self.IndustriesTable
        IndustriesFollowersTable = self.Followers_Statistics
        IndustriesFollowersTable = json_normalize(IndustriesFollowersTable[0]['followerCountsByIndustry']) 
        Industries = pd.merge(IndustriesTable,IndustriesFollowersTable,right_on='industry',left_on='$URN')
        Industries['total_followers'] = Industries['followerCounts.organicFollowerCount'] + Industries['followerCounts.paidFollowerCount']
        Industries = Industries.drop(['$URN','id','industry','followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        Industries = Industries.rename(columns = {"name.localized.en_US":"industries_name"}) 
        Industries.index = Industries.index.map(str)
        Industries = Industries.to_dict()
        return Industries
    
    def Generate_FollowersbySeniorities_List(self):
        SeniorityTable=self.SenioritiesTable
        SeniorityFollowersTable = self.Followers_Statistics
        SeniorityFollowersTable = json_normalize(SeniorityFollowersTable[0]['followerCountsBySeniority']) 
        Seniority = pd.merge(SeniorityTable,SeniorityFollowersTable,right_on='seniority',left_on='$URN')
        Seniority['total_followers'] = Seniority['followerCounts.organicFollowerCount'] + Seniority['followerCounts.paidFollowerCount']
        Seniority = Seniority.drop(['$URN','id','seniority','followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        SeniorityList = Seniority['name.localized.en_US'].tolist()
        FollowersList = Seniority['total_followers'].tolist()
        return SeniorityList, FollowersList
    
    def Generate_FollowersbySeniorities_Json(self):
        SeniorityTable=self.SenioritiesTable
        SeniorityFollowersTable = self.Followers_Statistics
        SeniorityFollowersTable = json_normalize(SeniorityFollowersTable[0]['followerCountsBySeniority']) 
        Seniority = pd.merge(SeniorityTable,SeniorityFollowersTable,right_on='seniority',left_on='$URN')
        Seniority['total_followers'] = Seniority['followerCounts.organicFollowerCount'] + Seniority['followerCounts.paidFollowerCount']
        Seniority = Seniority.drop(['$URN','id','seniority','followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        Seniority = Seniority.rename(columns = {"name.localized.en_US":"seniorties_name"}) 
        Seniority.index = Seniority.index.map(str)
        Seniority = Seniority.to_dict()
        return Seniority

    def Generate_FollowersbyAssocciation_Lists(self):
        AssocciationFollowersTable = self.Followers_Statistics
        AssocciationFollowersTable = (json_normalize(AssocciationFollowersTable[0]['followerCountsByAssociationType']))
        AssocciationFollowersTable.at[0,'associationType']="FOLLOWER"
        AssocciationFollowersTable['total_followers'] = AssocciationFollowersTable['followerCounts.organicFollowerCount'] + AssocciationFollowersTable['followerCounts.paidFollowerCount']
        AssocciationFollowersTable = AssocciationFollowersTable.drop(['followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        AssociationList = AssocciationFollowersTable['associationType'].tolist()
        FollowersList = AssocciationFollowersTable['total_followers'].tolist()
        return AssociationList, FollowersList

    def Generate_FollowersbyAssocciation_Json(self):
        AssocciationFollowersTable = self.Followers_Statistics
        AssocciationFollowersTable = (json_normalize(AssocciationFollowersTable[0]['followerCountsByAssociationType']))
        AssocciationFollowersTable.at[0,'associationType']="FOLLOWER"
        AssocciationFollowersTable['total_followers'] = AssocciationFollowersTable['followerCounts.organicFollowerCount'] + AssocciationFollowersTable['followerCounts.paidFollowerCount']
        Association = AssocciationFollowersTable.drop(['followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        Association = Association.rename(columns = {"name.localized.en_US":"associations_name"}) 
        Association.index = Association.index.map(str)
        Association = Association.to_dict()
        return Association
    
    def Generate_FollowersbyStaff_Lists(self):
        StaffFollowersTable = self.Followers_Statistics
        StaffFollowersTable = (json_normalize(StaffFollowersTable[0]['followerCountsByStaffCountRange']))
        StaffFollowersTable['total_followers'] = StaffFollowersTable['followerCounts.organicFollowerCount'] + StaffFollowersTable['followerCounts.paidFollowerCount']
        StaffFollowersTable = StaffFollowersTable.drop(['followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        StaffList = StaffFollowersTable['staffCountRange'].tolist()
        FollowersList = StaffFollowersTable['total_followers'].tolist()
        return StaffList, FollowersList 
    
    def Generate_FollowersbyStaff_Json(self):
        StaffFollowersTable = self.Followers_Statistics
        StaffFollowersTable = (json_normalize(StaffFollowersTable[0]['followerCountsByStaffCountRange']))
        StaffFollowersTable['total_followers'] = StaffFollowersTable['followerCounts.organicFollowerCount'] + StaffFollowersTable['followerCounts.paidFollowerCount']
        Association = StaffFollowersTable.drop(['followerCounts.organicFollowerCount','followerCounts.paidFollowerCount'],axis=1)
        Association.index = Association.index.map(str)
        Association = Association.to_dict()
        return Association

    def Generate_30days_shares_Lists(self):
        shares_30days=self.Shares_Statistics_30Days
        shares_30days['timeRange.start']=pd.to_datetime(shares_30days['timeRange.start'], unit='ms')
        shares_30days['Day'] = pd.DatetimeIndex(shares_30days['timeRange.start']).day
        shares_30days['Month'] = pd.DatetimeIndex(shares_30days['timeRange.start']).month
        shares_30days['Year'] = pd.DatetimeIndex(shares_30days['timeRange.start']).year
        shares_30days = shares_30days.rename(columns={"totalShareStatistics.engagement": "Engagement",
                                                     "totalShareStatistics.clickCount": "ClickCount",
                                                     "totalShareStatistics.uniqueImpressionsCount":"UniqueImpressionsCount",
                                                     "totalShareStatistics.shareCount":"ShareCount", 
                                                     "totalShareStatistics.commentCount":"CommentCount",
                                                     "timeRange.start":"Start Date",
                                                     "totalShareStatistics.impressionCount": "ImpressionCount"})
        shares_30days['Calculated Engagement'] = shares_30days['Engagement'] * shares_30days['ImpressionCount']
        shares_30days = shares_30days.drop(['organizationalEntity','Start Date','timeRange.end'], axis=1)
        Day = shares_30days['Day'].tolist()
        Month = shares_30days['Month'].tolist()
        Year = shares_30days['Year'].tolist()

        ImpressionCount  = shares_30days['ImpressionCount'].tolist()
        Engagement = shares_30days['Calculated Engagement'].tolist()
        ShareCount = shares_30days['ShareCount'].tolist()
        LikeCount = shares_30days['totalShareStatistics.likeCount'].tolist()
        MaxImpressionCount = np.max(ImpressionCount).astype(int).item()
        MaxEngagement = np.max(Engagement).astype(int).item()
        MaxShareCount = np.max(ShareCount).astype(int).item()
        MaxLikeCount  = np.max(LikeCount).astype(int).item()
        return Day,Month,Year,ImpressionCount,Engagement,ShareCount,LikeCount, MaxImpressionCount, MaxEngagement, MaxShareCount, MaxLikeCount

    def Generate_30days_shares_Json(self):
        shares_30days=self.Shares_Statistics_30Days
        shares_30days['timeRange.start']=pd.to_datetime(shares_30days['timeRange.start'], unit='ms')
        shares_30days['Day'] = pd.DatetimeIndex(shares_30days['timeRange.start']).day
        shares_30days['Month'] = pd.DatetimeIndex(shares_30days['timeRange.start']).month
        shares_30days['Year'] = pd.DatetimeIndex(shares_30days['timeRange.start']).year
        shares_30days = shares_30days.rename(columns={"totalShareStatistics.engagement": "Engagement",
                                                     "totalShareStatistics.clickCount": "ClickCount",
                                                     "totalShareStatistics.uniqueImpressionsCount":"UniqueImpressionsCount"
                                                     ,"totalShareStatistics.shareCount":"ShareCount", 
                                                     "totalShareStatistics.commentCount":"CommentCount",
                                                     "timeRange.start":"Start Date",
                                                     "totalShareStatistics.impressionCount": "ImpressionCount"})
        shares_30days['Calculated Engagement'] = shares_30days['Engagement'] * shares_30days['ImpressionCount']
        shares_30days = shares_30days.drop(['organizationalEntity','Start Date','timeRange.end','totalShareStatistics.likeCount','Calculated Engagement'], axis=1)
        shares_30days.index = shares_30days.index.map(str)
        shares_30days = shares_30days.to_dict()
        return shares_30days

    
if __name__ == '__main__':
    
    Access_Token = 'AQXsCVUdUweipF0PBULe4PlVrM7N3sXD595l5s3ZRm4Po4AYPCvxVOtr6CJ_kZ8Rl-nSb1Ti5JHy7xPQqjqOFCj1v4wSNlY_69AcffTfKwio631JxJdYM4Mrnsj4fGGe3ZHl35Wnl8OG6kcPkLg6ee2I0BvCebr_NHZF1jAdB9E-NO8HYAB4X3EjNX31q1Cba-zjOYywFSPQLNlnPp6FTiB9dE9vxTUGd5Q01h-gkFljSXthd0p4kZoh43psuH6mm_T7H9X9d0NJXoUek6kk5CfDy-BrYsGX5GW3BoGOcj9QXCz7qBqHTh8h8H_a04KFMUjbNvmRNJe1DL9NwAr9WKNdKX8FOw'
        
    Organization_ID = 'urn:li:organization:35639949'
    
    LinkedinPage = LinkedinWR(Access_Token = Access_Token,Organization_ID = Organization_ID) 