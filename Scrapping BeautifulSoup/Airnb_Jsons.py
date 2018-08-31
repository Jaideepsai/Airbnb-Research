
# coding: utf-8

# In[1]:


# Scrapping works only for images from AIrbnb http://insideairbnb.com/get-the-data.html excel
import os
import time
import json,urllib2
import urllib
from setuptools import setup
# import file
import pandas as pd
import numpy as np
data=pd.read_csv("/Users/jaideep/Desktop/Airbnb/Airbnb_Full_Project_Files_1/Data/main/listings 2.csv")
df = pd.DataFrame(data)[0:]
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# In[2]:


currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
folderName='ScrappedImages_' + str(currentMonth) + str(currentDay) + str(currentYear);
try:
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        os.makedirs('./'+ folderName +'/OccupancyJsons')
        os.makedirs('./'+ folderName +'/Images')
        os.makedirs('./'+ folderName +'/FullJsons')
except OSError:
    print ('Error: Creating directory of data')


# In[3]:


def fullJson(id):
    print id;
    listing_id=str(id);
    url="https://www.airbnb.com/rooms/"+listing_id
    page = requests.get(url)
    #parse html
    pageContents = BeautifulSoup(page.content, 'html.parser')
    #get all scripts containing json
    JSONTexts = pageContents.findAll("script", type="application/json")
    #loop through scripts
    for JSONText in JSONTexts:
        if JSONText.get('data-hypernova-key') == "spaspabundlejs":
            propInfoJSON = JSONText.next.replace('<!--','').replace('-->','').replace( u'\u2018', u"'").replace( u'\u2019', u"'")
    #parse text as json
    data = json.loads(propInfoJSON)
#     print data
    images(data,listing_id);
    fullJsonName = os.path.join(folderName + "/FullJsons", listing_id + "_full.json")
    with open(fullJsonName, 'w') as outfile:
#         dump full json
        json.dump(data, outfile)


# In[4]:


def images(json,id):
    time.sleep(np.random.randint(1,2))
    try:
        list_images=json["bootstrapData"]["reduxData"]["homePDP"]["listingInfo"]["listing"]["photos"];
        print len(list_images);
        for index,images in enumerate(list_images):
            imageName="";
            print index;
            if str(images["is_professional"]).lower() == "true":
                imageName=id +"_"+ str(index) + "_verified";
            else:
                imageName=id +"_"+ str(index) ;
#             print imageName;
            fullImagename = os.path.join(folderName + "/images", imageName + ".jpg")
#             print fullImagename;
            urllib.urlretrieve(str(images["xx_large"]), fullImagename)

    except:
        print "listing not available";
    
    


# In[6]:


def OccupancyJson(id):
    time.sleep(np.random.randint(1,2))
    print id;
    count_months=4;
    start_month=7;
    url = 'https://www.airbnb.com/api/v2/calendar_months?_format=with_conditions&count='+ str(count_months) +'&listing_id='+ str(id) + '&month='+str(start_month)+'&year=2018&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en'
#     url="https://www.airbnb.com/api/v2/calendar_months?_format=with_conditions&count=4&listing_id=2570620&month=7&year=2018&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en"
    print url;
    jsonName = os.path.join(folderName + "/OccupancyJsons", str(id)  + "_occupancy.json")
    urllib.urlretrieve(url, jsonName)


# In[8]:


for row in df.itertuples():
    OccupancyJson(row[1]);
    time.sleep(np.random.randint(1,3))
    fullJson(row[1]);
        

