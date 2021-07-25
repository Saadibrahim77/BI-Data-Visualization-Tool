import requests
import json
import pandas as pd
import numpy as np

class InstagramWR:

    Access_Tocken = None
    Page_ID = None
    Lifetime_Data = None
    FollowersData = None
    Daily_Data = None
    
    def __init__(self, tocken, ID ):
        self.Access_Tocken = tocken
        self.Page_ID = ID
        
    def Extract_Data(self):
        Lifetime_Media_URL = 'https://graph.facebook.com/'+ self.Page_ID +'?fields=insights.period(lifetime).metric(audience_gender_age,audience_locale,audience_city,audience_country),media{id,caption,media_url,timestamp,insights.since(30 days ago).metric(engagement,impressions,reach,saved)}&access_token=' + self.Access_Tocken
        response = requests.get(Lifetime_Media_URL)
        response.raise_for_status()
        Lifetime_Data = response.text
        Lifetime_Data = json.loads(response.text)
        Lifetime_Data = pd.json_normalize(Lifetime_Data['insights']['data'])
        Lifetime_Data = Lifetime_Data.set_index(['name'])
        Daily_Insights_URL = 'https://graph.facebook.com/'+ self.Page_ID +'?fields=followers_count,follows_count,media_count,insights.period(day).metric(reach,impressions,profile_views).since(30 days ago).until(now)&access_token=' + self.Access_Tocken
        response = requests.get(Daily_Insights_URL)
        response.raise_for_status()
        Followers_Daily_Data = json.loads(response.text)
        
        FollowersData = pd.json_normalize(Followers_Daily_Data)
        FollowersData = FollowersData.drop(columns = ['insights.data','id','insights.paging.previous','insights.paging.next'],axis = 1)
        Daily_Data = pd.json_normalize(Followers_Daily_Data['insights']['data'])
        
        self.Lifetime_Data = Lifetime_Data
        self.FollowersData = FollowersData
        self.Daily_Data = Daily_Data
        
        #return Lifetime_Data, FollowersData, Daily_Data
    
    def generate_Age_Gender_Lists(self):
        PageAgeGenderParameter = self.Lifetime_Data.loc['audience_gender_age']['values']
        PageAgeGenderTable = pd.DataFrame(pd.json_normalize(PageAgeGenderParameter))
        PageAgeGenderTable = PageAgeGenderTable.drop(['end_time'], axis = 1)
        PageAgeGenderTable = PageAgeGenderTable.melt( var_name='Attribute', value_name='Value')
        PageAgeGenderTable = PageAgeGenderTable.dropna(subset=['Value'])
        temp = PageAgeGenderTable["Attribute"].str.split(".", n = 2, expand = True)
        PageAgeGenderTable["Gender"] = temp[1]
        PageAgeGenderTable['Age'] = temp[2]
        PageAgeGenderTable = PageAgeGenderTable.drop(['Attribute'], axis = 1)
        PageAgeGenderTable = PageAgeGenderTable[PageAgeGenderTable.Gender != 'U']
        PageAgeGenderTable = PageAgeGenderTable.pivot(index='Age',columns='Gender',values='Value') 
        PageAgeGenderTable = PageAgeGenderTable.reset_index()
        return PageAgeGenderTable
    
    def generate_Age_Gender_Json(self):
        PageAgeGenderParameter = self.Lifetime_Data.loc['audience_gender_age']['values']
        PageAgeGenderTable = pd.DataFrame(pd.json_normalize(PageAgeGenderParameter))
        PageAgeGenderTable = PageAgeGenderTable.drop(['end_time'], axis = 1)
        PageAgeGenderTable = PageAgeGenderTable.melt( var_name='Attribute', value_name='Value')
        PageAgeGenderTable = PageAgeGenderTable.dropna(subset=['Value'])
        temp = PageAgeGenderTable["Attribute"].str.split(".", n = 2, expand = True)
        PageAgeGenderTable["Gender"] = temp[1]
        PageAgeGenderTable['Age'] = temp[2]
        PageAgeGenderTable = PageAgeGenderTable.drop(['Attribute'], axis = 1)
        PageAgeGenderTable = PageAgeGenderTable[PageAgeGenderTable.Gender != 'U']
        PageAgeGenderTable = PageAgeGenderTable.pivot(index='Age',columns='Gender',values='Value') 
        PageAgeGenderTable = PageAgeGenderTable.reset_index()
        PageAgeGenderTable.index = PageAgeGenderTable.index.map(str)
        PageAgeGenderDict = PageAgeGenderTable.to_dict()
        return PageAgeGenderDict
    
    
    def generate_Languages_Lists(self):
        LanguageParameter = self.Lifetime_Data.loc['audience_locale']['values']
        LanguagesTable = pd.DataFrame(pd.json_normalize(LanguageParameter))
        LanguagesTable = LanguagesTable.drop(['end_time'], axis = 1)
        LanguagesTable = LanguagesTable.melt(var_name='Attribute',value_name='Value')
        temp = LanguagesTable["Attribute"].str.split(".", n = 2, expand = True)
        LanguagesTable["Language"] = temp[1]
        LanguagesTable = LanguagesTable.drop(['Attribute'], axis = 1)
        LanguagesTable['Value'] = LanguagesTable.Value.astype(str)
        LanguagesList = LanguagesTable['Language'].tolist()
        LanguagesTable['Value'] = LanguagesTable.Value.astype(int)
        FollowersbyLanguage = LanguagesTable['Value'].tolist()
        return LanguagesList, FollowersbyLanguage

    def generate_Languages_Json(self):
        LanguageParameter = self.Lifetime_Data.loc['audience_locale']['values']
        LanguagesTable = pd.DataFrame(pd.json_normalize(LanguageParameter))
        LanguagesTable = LanguagesTable.drop(['end_time'], axis = 1)
        LanguagesTable = LanguagesTable.melt(var_name='Attribute',value_name='Value')
        temp = LanguagesTable["Attribute"].str.split(".", n = 2, expand = True)
        LanguagesTable["Language"] = temp[1]
        LanguagesTable = LanguagesTable.drop(['Attribute'], axis = 1)
        LanguagesTable['Value'] = LanguagesTable.Value.astype(str)
        LanguagesList = LanguagesTable['Language'].tolist()
        LanguagesTable['Value'] = LanguagesTable.Value.astype(int)
        FollowersbyLanguage = LanguagesTable['Value'].tolist()
        LanguagesTable.index = LanguagesTable.index.map(str)
        LanguagesDict = LanguagesTable.to_dict()
        return LanguagesDict

    
    def generate_City_Lists(self):
        CitiesParameter = self.Lifetime_Data.loc['audience_city']['values']
        CitiesTable = pd.DataFrame(pd.json_normalize(CitiesParameter))
        CitiesTable = CitiesTable.drop(['end_time'],axis=1)
        CitiesTable = CitiesTable.melt(var_name='City',value_name='Value')
        temp = CitiesTable["City"].str.split(".", n = 2, expand = True)
        CitiesTable["City"] = temp[1]
        temp = CitiesTable['City'].str.split(',', n=1, expand=True)
        CitiesTable["City"] = temp
        citiesList = CitiesTable['City'].tolist()
        FollowersbyCity = CitiesTable['Value'].tolist()
        return citiesList, FollowersbyCity
    
    def generate_City_Json(self):
        CitiesParameter = self.Lifetime_Data.loc['audience_city']['values']
        CitiesTable = pd.DataFrame(pd.json_normalize(CitiesParameter))
        CitiesTable = CitiesTable.drop(['end_time'],axis=1)
        CitiesTable = CitiesTable.melt(var_name='City',value_name='Value')
        temp = CitiesTable["City"].str.split(".", n = 2, expand = True)
        CitiesTable["City"] = temp[1]
        temp = CitiesTable['City'].str.split(',', n=1, expand=True)
        CitiesTable["City"] = temp
        CitiesTable.index = CitiesTable.index.map(str)
        CitiesDict = CitiesTable.to_dict()
        return CitiesDict
    

    def generate_followers_Lists(self):
        FollowersDataTable = self.FollowersData
        FollowersDataTable.rename(columns = {'follows_count':'Following','followers_count':'Followers','media_count':'Number of Posts'},inplace = True)
        NoOfFollowerslist = FollowersDataTable.loc[0][0].tolist()
        NoOfFollowingList = FollowersDataTable.loc[0][1].tolist()
        NoOfPosts = FollowersDataTable.loc[0][2].tolist()
        return NoOfFollowerslist,NoOfFollowingList,NoOfPosts
       
    def generate_followers_Json(self):
        FollowersDataTable = self.FollowersData
        FollowersDataTable.rename(columns = {'follows_count':'Following','followers_count':'Followers','media_count':'Number of Posts'},inplace = True)
        FollowersDataTable.index = FollowersDataTable.index.map(str)
        FollowersDict = FollowersDataTable.to_dict()
        return FollowersDict
    

    def generate_Countries_Lists(self):
        Countries = self.Lifetime_Data.loc['audience_country']['values']
        Countries_Table = pd.DataFrame(pd.json_normalize(Countries))
        Countries_Table = Countries_Table.drop(['end_time'],axis=1)
        Countries_Table = Countries_Table.melt(var_name='Country',value_name='Value')
        temp = Countries_Table["Country"].str.split(".", n = 2, expand = True)
        Countries_Table["Country"] = temp[1]
        countriesList = Countries_Table['Country'].tolist()
        FollowersbyCountry = Countries_Table['Value'].tolist()
        return countriesList,FollowersbyCountry
    
    def generate_Countries_Json(self):
        Countries = self.Lifetime_Data.loc['audience_country']['values']
        Countries_Table = pd.DataFrame(pd.json_normalize(Countries))
        Countries_Table = Countries_Table.drop(['end_time'],axis=1)
        Countries_Table = Countries_Table.melt(var_name='Country',value_name='Value')
        temp = Countries_Table["Country"].str.split(".", n = 2, expand = True)
        Countries_Table["Country"] = temp[1]
        Countries_Table.index = Countries_Table.index.map(str)
        CountriesDict = Countries_Table.to_dict()
        return CountriesDict
    
    
    def generate_Days_Lists(self):
        DaysMetricsTable = self.Daily_Data.drop(['period','description','id','title'],axis=1)
        DaysMetricsTable = DaysMetricsTable.set_index('name')
        DaysMetricsTable = DaysMetricsTable.loc[['reach','impressions','profile_views']]
        DaysMetricsTable = DaysMetricsTable.reset_index()
        DayInsights = pd.json_normalize(DaysMetricsTable.loc[0]['values'])
        DayInsights['Parameter'] = DaysMetricsTable.loc[0]['name']
        for Parameter in range(1,DaysMetricsTable.shape[0]):
            Temp = pd.json_normalize(DaysMetricsTable.loc[Parameter]['values'])
            Temp['Parameter'] = DaysMetricsTable.loc[Parameter]['name']
            DayInsights = DayInsights.append(Temp)
        DayInsights = DayInsights.reset_index()
        DayInsights = DayInsights.drop('index',axis=1)
        tempDate = DayInsights["end_time"].str.split(":", n = 2, expand = True)
        tempDate = tempDate[0]    
        tempDate = DayInsights["end_time"].str.split("T", n = 2, expand = True)
        tempDate = tempDate[0]
        DayInsights['end_time'] = tempDate
        startDate = DayInsights['end_time'][0]
        endDate = DayInsights['end_time'][DayInsights.shape[0]-1]
        df = pd.DataFrame({'my_dates':pd.date_range(startDate, endDate)})
        df['day_of_week'] = df['my_dates'].dt.day_name()
        DayInsights = DayInsights.pivot_table(index = ['end_time'],columns = 'Parameter',values='value')
        DayInsights = DayInsights.reset_index()
        
        new = pd.DataFrame(df['day_of_week'])
        DayInsights['Day of Week'] = new
        DayInsights = DayInsights.groupby(['Day of Week']).agg(['sum'])  
        DayInsights = DayInsights.reset_index()
        DayInsights.columns = ['Day of Week', 'end_time', 'impressions', 'profile_views', 'reach']


        ProfileViewslist = DayInsights['profile_views'].tolist()
        impressionslist = DayInsights['impressions'].tolist()
        reachlist = DayInsights['reach'].tolist()
        DayOfWeeklist = DayInsights['Day of Week'].tolist()
        totalreach = np.sum(reachlist)
        totalimpressions = np.sum(impressionslist)
        totalprofileviews = np.sum(ProfileViewslist)
        
        maxProfileViewslist = np.max(ProfileViewslist).astype(int).item() 
        maximpressionslist = np.max(impressionslist).astype(int).item()
        maxreachlist = np.max(reachlist).astype(int).item()
        return ProfileViewslist, impressionslist, reachlist, DayOfWeeklist, totalreach, totalimpressions, totalprofileviews,maximpressionslist,maxProfileViewslist,maxreachlist,DayInsights

    def generate_Days_Json(self):
        DaysMetricsTable = self.Daily_Data.drop(['period','description','id','title'],axis=1)
        DaysMetricsTable = DaysMetricsTable.set_index('name')
        DaysMetricsTable = DaysMetricsTable.loc[['reach','impressions','profile_views']]
        DaysMetricsTable = DaysMetricsTable.reset_index()
        DayInsights = pd.json_normalize(DaysMetricsTable.loc[0]['values'])
        DayInsights['Parameter'] = DaysMetricsTable.loc[0]['name']
        for Parameter in range(1,DaysMetricsTable.shape[0]):
            Temp = pd.json_normalize(DaysMetricsTable.loc[Parameter]['values'])
            Temp['Parameter'] = DaysMetricsTable.loc[Parameter]['name']
            DayInsights = DayInsights.append(Temp)
        DayInsights = DayInsights.reset_index()
        DayInsights = DayInsights.drop('index',axis=1)
        tempDate = DayInsights["end_time"].str.split(":", n = 2, expand = True)
        tempDate = tempDate[0]    
        tempDate = DayInsights["end_time"].str.split("T", n = 2, expand = True)
        tempDate = tempDate[0]
        DayInsights['end_time'] = tempDate
        startDate = DayInsights['end_time'][0]
        endDate = DayInsights['end_time'][DayInsights.shape[0]-1]
        df = pd.DataFrame({'my_dates':pd.date_range(startDate, endDate)})
        df['day_of_week'] = df['my_dates'].dt.day_name()
        DayInsights = DayInsights.pivot_table(index = ['end_time'],columns = 'Parameter',values='value')
        DayInsights = DayInsights.reset_index()
        new = pd.DataFrame(df['day_of_week'])
        DayInsights['Day of Week'] = new
        DayInsights.index = DayInsights.index.map(str)
        DayInsights_Dict = DayInsights.to_dict()
        return DayInsights_Dict
    