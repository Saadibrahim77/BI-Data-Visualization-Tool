from flask import Blueprint,Flask,url_for,redirect,render_template,request,session
import requests
import json
from Model.Organization import Organization
from pandas import json_normalize
from Data.CustomerSegmentation import CustomerSegmentation
from Data.ProductAffinity import ProductAffinity
import os
Platform = Blueprint("PlatForm",__name__)

#UPLOAD_FOLDER = 'static/files'
#Platform.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


@Platform.route("/customerview")
def GetCustomerView():
    return render_template("customerseg.html")

@Platform.route("/productview")
def GetProductView():
    return render_template("product.html")


@Platform.route("/customers",methods=["POST"])
def UploadCustomerFile():

    customerseg =CustomerSegmentation()

    df,clusterlabels,clustervalues,amountlabels,amountvalues = customerseg.CustomerValues()
      # get the uploaded file
    uploaded_file = request.files['file']
    print(uploaded_file)
    if uploaded_file.filename != '':
           #file_path = os.path.join(Platform.config['UPLOAD_FOLDER'], uploaded_file.filename)
           #print(file_path)
           # set the file path
           #uploaded_file.save(file_path)
          # save the file
          pass
    return render_template('customerseggraph.html',clusterlabels=clusterlabels,clustervalues=clustervalues,amountlabels=amountlabels,amountvalues=amountvalues )



@Platform.route("/products",methods=["POST"])
def UploadProductFile():
    products =  ProductAffinity()
    df,df2= products.GetProductValues()
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':

        #file_path = os.path.join(Platform.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print(file_path)
        #uploaded_file.save(file_path)
          # save the file
          pass
    return render_template('productgraph.html', column_names=df.columns.values, row_data=list(df.values.tolist())
                                                      , zip=zip , column_names2=df2.columns.values, row_data2=list(df2.values.tolist()))



 
@Platform.route('/Instagram/AccessToken/<string:access_token>')
def Instagram(access_token):
     session["Access_token"] = access_token
     session["Platform"] = "insta"
     return GetInstagramPages(access_token)


    
def GetInstagramPages(access_token):
    #print(access_token)
    fields = "&fields=accounts{access_token,name,picture.type(large){url}, instagram_business_account}"
    url = "https://graph.facebook.com/me?access_token=" + access_token + fields
    #"https://api.thedogapi.com/v1/breeds"
    response = requests.get(url)
    with open('Accounts.json') as json_file:
       data = json.load(json_file)
    Accounts = (data['accounts']['data'])
    Error = response.raise_for_status()
    #Accounts = (json_normalize(response.json()['accounts']['data']))
    return  render_template('InstaPageView.html',Pages =response.json()['accounts']['data'])


def GetLinkedInAuthURL():
     
     #print(url)
     return url

    
@Platform.route('/Linkedin/Auth')
def LinkedIn():
    url ='https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77g922eb37z4ic&redirect_uri=http%3A%2F%2Flocalhost:5432%2Fplatform%2Flinkedin%2Fverify&scope=r_organization_social%2Cr_1st_connections_size%2Cr_emailaddress%2Cr_ads_reporting%2Crw_organization_admin%2Cr_liteprofile%2Cr_basicprofile%2Crw_ads%2Cr_ads%2Cw_member_social%2Cw_organization_social'
    return redirect(url)
    
    
@Platform.route('/linkedin/verify/')
def LinkedInVerify():
    code = request.args.get("code")
    client_id = '77g922eb37z4ic'
    client_secret = 'ffThXOiLGRwg2CbK'
    url  = 'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code=' + code + '&redirect_uri=http%3A%2F%2Flocalhost:5432%2Fplatform%2Flinkedin%2Fverify&client_id=' + client_id + '&client_secret=' + client_secret
    ret = requests.post(url)
    response_content = ret.content.decode('utf8').replace("'", '"')
    json_content = json.loads(response_content)
    access_token = json_content['access_token']
    session["Access_token"] = access_token
    session["Platform"] = "linkedin"
    return (GetLinkedinPages())


def GetLinkedinPages():
    GetPages = "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee&role=ADMINISTRATOR&state=APPROVED&projection=(*,elements*(*,organizationalTarget~(*,logoV2(original~:playableStreams,cropped~:playableStreams,cropInfo)))) "#"https://api.linkedin.com/v2/organizationAcls?q=roleAssignee"
    #Access_Token = "AQVJ58MQcCZnKeCK2uxq6mLFsA0aYTaYiYnJYqS4sF7TKFMQitvj09crUMKFB-ofUV5jLMhhGIq6f9JGiX81mGld4FsbYu53959QTmf3Kt1D6tLQelZKnOtB8EOatvRnx-1ZPmJbZJNXx5hHytLC70xRADL4QREWmbow9IbmJ9S7k5N6mAW6yxBAaYy2u5C0HkdqR04TaV_-zBZVaWY3_7Rakn27lauhuAEwGxPlg93tGV5JXE1nnMIpr2qDeRcX7xWZC9UTY-BAMDCncRxKKcSxphJMoHJBWqDbujhqAmKSIrwH_pt0rWnWlctgp-pKdZlS7cwRoBKeQ1AIO6Fa0oipbctP6g"
    response = requests.get(GetPages,headers={"X-Restli-Protocol-Version":"2.0.0","Authorization":"Bearer " + session["Access_token"]})
    Pages = response.json()
    
   
    Organizations_list = []
    for i in range(len(Pages['elements'])):
        page_name = Pages['elements'][i]['organizationalTarget~']['localizedName']
        page_id = Pages['elements'][i]['organizationalTarget']
        page_pic = Pages['elements'][i]['organizationalTarget~']['logoV2']['original~']['elements'][0]['identifiers'][0]['identifier']
        organ = Organization(page_name,page_id,page_pic) 
        Organizations_list.append(organ)
      

    return render_template("LinkedInPageView.html",Pages = Organizations_list)







