import sys
import copy
import logging
# Pulling in and scraping html data
from bs4 import BeautifulSoup
import json
import urllib
import urllib.request
from urllib3 import ProxyManager, make_headers, PoolManager

# Reading PDF and pulling data from PDF
import PyPDF2
import io
import re
from datetime import datetime
import collections

# Storing Data
from tinydb import TinyDB, Query
from json2html import *

# Sending Email
import html
import win32com.client as win32


# Init logging
logging.basicConfig(handlers=[logging.FileHandler('scraper.log', 'w', 'utf-8')], format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)

class DARPAScraper:
    # Constructor - specifies the database object/file that will be used 
    def __init__(self,databaseObject):
        self.database = databaseObject
    
    # Function that constructs the URL for darpa staff members. Used for getting projects that the project manager is managing
    def createAboutURL(self,name):
        aboutBaseURL = 'https://www.darpa.mil/staff/'
        tempName = name.split(' ')
        if(len(tempName) ==4 ):
            del tempName[2]
        finalName = tempName[0]
        finalName = finalName[:-1]
        finalName = finalName + '-' + tempName[1] + '-' + tempName[2]
        finalName=finalName.lower()
        aboutURL = aboutBaseURL + finalName
        return aboutURL

    # Function that returns html data using the beautiful soup library, so parsing and scraping can be done
    def returnSoupData(self,url):
        # find any proxies and set auth username and password. If on NG network most likly going throug a proxy
        findProxies = urllib.request.getproxies()
        default_headers = make_headers(proxy_basic_auth=sys.argv[1] + ":" + sys.argv[2]) # NG username and password should be passed in via command line

        # init url and http headers to make it look like a legit request from a chrome broswer. Some websites reject python itself from accessing the webpage 
        # so a workaround is to specify http headers to make it look legit    
        URL = url
        headers =   {   
                        'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://www.google.com/',
                        'upgrade-insecure-requests': '1',
                        'sec-fetch-dest' : 'document',
                        'sec-fetch-mode' : 'navigate',
                        'sec-fetch-site': 'cross-site',
                        'proxy-connection': 'Keep-Alive'
                    }

        # If there are not found proxies perform a regular GET request and return html data. If there is a proxy an additonal step is used to auth with proxy before the GET request
        if(findProxies == {}):
            httpNoProxy = PoolManager()
            r = httpNoProxy.request('GET', URL, headers=headers) 
            htmlData = BeautifulSoup(r.data, 'html.parser')
        else:
            proxy = next(iter(findProxies.values()))
            http = ProxyManager(proxy, proxy_headers=default_headers)
            r = http.request('GET', URL, headers=headers)
            htmlData = BeautifulSoup(r.data, 'html.parser')

        return htmlData

    # Function that performs a GET request but takes into consideration any proxies     
    def getRequest(self, url):

        # find any proxies and set auth username and password. If on NG network most likly going throug a proxy
        findProxies = urllib.request.getproxies()
        default_headers = make_headers(proxy_basic_auth=sys.argv[1] + ":" + sys.argv[2]) # NG username and password should be passed in via command line


        # init url and http headers to make it look like a legit request from a chrome broswer. Some websites reject python itself from accessing the webpage 
        # so a workaround is to specify http headers to make it look legit
        URL = url
        headers =   {   
                        'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://www.google.com/',
                        'upgrade-insecure-requests': '1',
                        'sec-fetch-dest' : 'document',
                        'sec-fetch-mode' : 'navigate',
                        'sec-fetch-site': 'cross-site',
                        'proxy-connection': 'Keep-Alive'
                    }


        # If there are not found proxies perform a regular GET request. If there is a proxy an additonal step is used to auth with proxy before the GET request
        if(findProxies == {}):
            httpNoProxy = PoolManager()
            requestData = httpNoProxy.request('GET', URL, headers=headers) 
        else:
            proxy = next(iter(findProxies.values()))
            http = ProxyManager(proxy, proxy_headers=default_headers)
            requestData = http.request('GET', URL, headers=headers)

        return requestData

    # function that performs a get request for getting pdfs. Used when getting specific pdfs associated with DARPA BAA's. The difference between the getRequest function and this function is the preload_content parameter 
    # in the request function is set to false. Setting preload_content to False means that urllib3 will stream the response content which is good for pdf content
    def getRequestPDF(self, url):
        # find any proxies and set auth username and password. If on NG network most likly going throug a proxy
        findProxies = urllib.request.getproxies()
        default_headers = make_headers(proxy_basic_auth=sys.argv[1] + ":" + sys.argv[2]) # NG username and password should be passed in via command line

        # init url and http headers to make it look like a legit request from a chrome broswer. Some websites reject python itself from accessing the webpage 
        # so a workaround is to specify http headers to make it look legit
        URL = url
        headers =   {   
                        'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://www.google.com/',
                        'upgrade-insecure-requests': '1',
                        'sec-fetch-dest' : 'document',
                        'sec-fetch-mode' : 'navigate',
                        'sec-fetch-site': 'cross-site',
                        'proxy-connection': 'Keep-Alive'
                    }
        

        # If there are not found proxies perform a regular GET request. If there is a proxy an additonal step is used to auth with proxy before the GET request
        if(findProxies == {}):
            httpNoProxy = PoolManager()
            requestData = httpNoProxy.request('GET', URL, headers=headers,preload_content=False)  
        else:
            proxy = next(iter(findProxies.values()))
            http = ProxyManager(proxy, proxy_headers=default_headers)
            requestData = http.request('GET', URL, headers=headers, preload_content=False) 
        

        return requestData



    # Function that scrapes all MTO managers from DARPA website
    def GetMTOProgramManagers(self,databaseTableName):
        mto  = self.database.table(databaseTableName,cache_size=0) # init database table
        mto_lastupdated = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for mto
        pageNumber = 0  # keeps track of pages
        URL = 'https://www.darpa.mil/about-us/offices/mto/staff-list?PP=' + str(pageNumber) # Starting URL to get first page of MTO Program Managers
        full_data=[] # Holds results of scraper, list of JSON strings

        # Try Scraping, if error, abort
        try: 
            while True:
                soup = self.returnSoupData(URL) # Get html data on page

                # find the dnn_ctr486_StaffList_dlProgramManagers id. This is a table that holds all the mto managers. 
                # If the listingTable is not found, that means we have gone through all the pages and scraped all the mto manager data, so we break out of the loop 
                listingTable  = soup.find(id='dnn_ctr486_StaffList_dlProgramManagers')
                if(not listingTable):
                    break

                # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM
                managers = listingTable.find_all('div', class_='listing__right')

                # For every manager found on page
                for manager in managers:
                    interestList = []
                    programsList = []

                    name = manager.find('a') # Get the manager name
                    title = manager.find('div', class_='listing__position') # Get the managers title
                    description = manager.find('div', class_="listing__copy") # Get the managers description 

                    # Get managers interests
                    interests = manager.find_all('a',class_='listing__tag-item listing__tag-link') 
                    for interest in interests:
                        (interestList.append(interest.text))


                    # Go to the managers about page and pull program names that the manager is a part of
                    programSoup = self.returnSoupData(self.createAboutURL(name.text))
                    programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                    if(programs):
                        programNames = programs.find_all('div', class_='sidebar__link')
                        for programName in programNames:
                            programsList.append(programName.text)

                    # Store results in JSON Object and append to full data
                    jsonDataTemp = {
                        "name" : name.text,
                        "title" : title.text,
                        "description" : description.text,
                        "interests" : interestList,
                        "programs" : programsList
                    }
                    full_data.append(jsonDataTemp)
                    logging.info(jsonDataTemp)

                # Move to next page
                pageNumber = pageNumber + 1
                URL = 'https://www.darpa.mil/about-us/offices/mto/staff-list?PP=' + str(pageNumber)

            # Clear the database table and insert the new updated data
            logging.info("Clearing and Updating Database File")
            mto.truncate()
            mto.insert_multiple(full_data)

            mto_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            mto_lastupdated.insert({'lastupdated' : time})
            

        # if an error occurs return
        except:
            logging.error("Error Scraping MTO Managers")
            return

        logging.info("MTO Managers Scrape Successful")


    # Function that scrapes all I2O managers from DARPA website
    def GetI2OProgramManagers(self,databaseTableName):
        i2o  = self.database.table(databaseTableName,cache_size=0) # init database table
        i2o_lastupdated = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for i2o
        pageNumber = 0 # keeps track of pages
        URL = 'https://www.darpa.mil/about-us/offices/i2o/staff-list?PP=' + str(pageNumber) # Starting URL to get first page of I2O Program Managers
        full_data=[] # Holds results of scraper, list of JSON strings

        # Try Scraping, if error, abort
        try:
            while True:
                soup = self.returnSoupData(URL) # Get html data on page

                # find the dnn_ctr480_StaffList_dlProgramManagers id. This is a table that holds all the i2o managers. 
                # If the listingTable is not found, that means we have gone through all the pages and scraped all the i2o manager data, so we break out of the loop 
                listingTable  = soup.find(id='dnn_ctr480_StaffList_dlProgramManagers')
                if(not listingTable):
                    break

                # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM
                managers = listingTable.find_all('div', class_='listing__right')

                # For every manager found on page
                for manager in managers:
                    interestList = []
                    programsList = []

                    name = manager.find('a') # Get the manager name
                    title = manager.find('div', class_='listing__position') # Get the managers title
                    description = manager.find('div', class_="listing__copy") # Get the managers description 

                    # Get managers interests
                    interests = manager.find_all('a',class_='listing__tag-item listing__tag-link')
                    for interest in interests:
                        (interestList.append(interest.text))

                    # Go to the managers about page and pull program names that the manager is a part of
                    programSoup = self.returnSoupData(self.createAboutURL(name.text))
                    programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                    if(programs):
                        programNames = programs.find_all('div', class_='sidebar__link')
                        for programName in programNames:
                            programsList.append(programName.text)

                    # Store results in JSON Object and append to full data
                    jsonDataTemp = {
                        "name" : name.text,
                        "title" : title.text,
                        "description" : description.text,
                        "interests" : interestList,
                        "programs" : programsList
                    }
                    full_data.append(jsonDataTemp)
                    logging.info(jsonDataTemp)

                # Move to next page
                pageNumber = pageNumber + 1
                URL = 'https://www.darpa.mil/about-us/offices/i2o/staff-list?PP=' + str(pageNumber)

            # if scrape was successful clear the database table and insert the new updated data
            logging.info("Clearing and Updating Database File")
            i2o.truncate()
            i2o.insert_multiple(full_data)

            i2o_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            i2o_lastupdated.insert({'lastupdated' : time})

         # if an error occurs return   
        except:
            logging.error("Error Scraping I2O Managers")
            return
        
        logging.info("I2O Managers Scrape Successful")

    # Function that scrapes all BTO managers from DARPA website
    def GetBTOProgramManagers(self, databaseTableName):

        bto = self.database.table(databaseTableName,cache_size=0) # init database table
        bto_lastupdated = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for bto
        pageNumber=0 # keeps track of pages
        URL = 'https://www.darpa.mil/about-us/offices/bto/staff-list?PP=' + str(pageNumber)  # Starting URL to get first page of BTO Program Managers
        full_data=[] # Holds results of scraper, list of JSON strings

        # Try Scraping, if error, abort
        try:
            while True:
                soup = self.returnSoupData(URL)# Get html data on page

                # find the dnn_ctr465_StaffList_dlProgramManagers id. This is a table that holds all the i2o managers. 
                # If the listingTable is not found, that means we have gone through all the pages and scraped all the i2o manager data, so we break out of the loop
                listingTable  = soup.find(id='dnn_ctr465_StaffList_dlProgramManagers')
                if(not listingTable):
                    break

                # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM
                managers = listingTable.find_all('div', class_='listing__right')
                # For every manager found on page
                for manager in managers:
                    interestList = []
                    programsList = []

                    name = manager.find('a') # Get the manager name
                    title = manager.find('div', class_='listing__position') # Get the managers title
                    description = manager.find('div', class_="listing__copy") # Get the managers description 

                    # Get managers interests
                    interests = manager.find_all('a',class_='listing__tag-item listing__tag-link')
                    for interest in interests:
                        (interestList.append(interest.text))

                    # Go to the managers about page and pull program names that the manager is a part of
                    programSoup = self.returnSoupData(self.createAboutURL(name.text))
                    programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                    if(programs):
                        programNames = programs.find_all('div', class_='sidebar__link')
                        for programName in programNames:
                            programsList.append(programName.text)

                    # Store results in JSON Object and append to full data
                    jsonDataTemp = {
                        "name" : name.text,
                        "title" : title.text,
                        "description" : description.text,
                        "interests" : interestList,
                        "programs" : programsList
                    }
                    full_data.append(jsonDataTemp)
                    logging.info(jsonDataTemp)
                    

                # Move to next page
                pageNumber = pageNumber + 1
                URL = 'https://www.darpa.mil/about-us/offices/bto/staff-list?PP=' + str(pageNumber)

            # if scrape was successful clear the database table and insert the new updated data

            logging.info("Clearing and Updating Database File")
            bto.truncate()
            bto.insert_multiple(full_data)

            bto_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            bto_lastupdated.insert({'lastupdated' : time})

        # if an error occurs return    
        except:
            logging.error("Error Scraping BTO Managers")
            return

        logging.info("BTO Managers Scrape Successful")


    # Function that scrapes all STO managers from DARPA website
    def GetSTOProgramManagers(self, databaseTableName):
        sto = self.database.table(databaseTableName,cache_size=0) # init database table
        sto_lastupdated = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for sto
        pageNumber=0 # keeps track of page
        URL = 'https://www.darpa.mil/about-us/offices/sto/staff-list?PP=' + str(pageNumber) # Starting URL to get first page of STO Program Managers
        full_data=[] # Holds results of scraper, list of JSON strings

        # Try Scraping, if error, abort
        try:
            while True:
                soup = self.returnSoupData(URL) # Get html data on page

                # find the dnn_ctr492_StaffList_dlProgramManagers id. This is a table that holds all the sto managers. 
                # If the listingTable is not found, that means we have gone through all the pages and scraped all the sto manager data, so we break out of the loop
                listingTable  = soup.find(id='dnn_ctr492_StaffList_dlProgramManagers')
                if(not listingTable):
                    break

                # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM   
                managers = listingTable.find_all('div', class_='listing__right')
                # For every manager found on page
                for manager in managers:
                    interestList = []
                    programsList = []

                    name = manager.find('a')  # Get the manager name
                    title = manager.find('div', class_='listing__position') # Get the managers title
                    description = manager.find('div', class_="listing__copy") # Get the managers description 

                    # Get managers interests
                    interests = manager.find_all('a',class_='listing__tag-item listing__tag-link')
                    for interest in interests:
                        (interestList.append(interest.text))

                    # Go to the managers about page and pull program names that the manager is a part of
                    programSoup = self.returnSoupData(self.createAboutURL(name.text))
                    programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                    if(programs):
                        programNames = programs.find_all('div', class_='sidebar__link')
                        for programName in programNames:
                            programsList.append(programName.text)

                    # Store results in JSON Object and append to full data
                    jsonDataTemp = {
                        "name" : name.text,
                        "title" : title.text,
                        "description" : description.text,
                        "interests" : interestList,
                        "programs" : programsList
                    }
                    full_data.append(jsonDataTemp)
                    logging.info(jsonDataTemp)

                # Move to next page
                pageNumber = pageNumber + 1
                URL = 'https://www.darpa.mil/about-us/offices/sto/staff-list?PP=' + str(pageNumber)
            
            # if scrape was successful clear the database table and insert the new updated data
            logging.info("Clearing and Updating Database File")
            sto.truncate()
            sto.insert_multiple(full_data)

            sto_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            sto_lastupdated.insert({'lastupdated' : time})

        # if an error occurs return    
        except:
            logging.error("Error Scraping STO Managers")
            return 
        logging.info("STO Managers Scrape Successful")


    # Function that scrapes all TTO managers from DARPA website
    def GetTTOProgramManagers(self, databaseTableName):
        tto = self.database.table(databaseTableName,cache_size=0) # init database table
        tto_lastupdated = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for tto
        pageNumber=0 # keeps track of page
        URL = 'https://www.darpa.mil/about-us/offices/tto/staff-list?PP=' + str(pageNumber) # Starting URL to get first page of TTO Program Managers
        full_data=[] # Holds results of scraper, list of JSON strings

        # Try Scraping, if error, abort mission
        try:
            while True:
                soup = self.returnSoupData(URL) # Get html data on page

                # find the dnn_ctr498_StaffList_dlProgramManagers id. This is a table that holds all the TTO managers. 
                # If the listingTable is not found, that means we have gone through all the pages and scraped all the TTO manager data, so we break out of the loop
                listingTable  = soup.find(id='dnn_ctr498_StaffList_dlProgramManagers')
                if(not listingTable):
                    break
                
                # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM
                managers = listingTable.find_all('div', class_='listing__right')

                # For every manager found on page
                for manager in managers:
                    interestList = []
                    programsList = []


                    name = manager.find('a') # Get the manager name
                    title = manager.find('div', class_='listing__position') # Get the managers title
                    description = manager.find('div', class_="listing__copy") # Get the managers description 

                    # Get managers interests
                    interests = manager.find_all('a',class_='listing__tag-item listing__tag-link')
                    for interest in interests:
                        (interestList.append(interest.text))

                    # Go to the managers about page and pull program names that the manager is a part of
                    programSoup = self.returnSoupData(self.createAboutURL(name.text))
                    programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                    if(programs):
                        programNames = programs.find_all('div', class_='sidebar__link')
                        for programName in programNames:
                            programsList.append(programName.text)

                    # Store results in JSON Object and append to full data
                    jsonDataTemp = {
                        "name" : name.text,
                        "title" : title.text,
                        "description" : description.text,
                        "interests" : interestList,
                        "programs" : programsList
                    }
                    full_data.append(jsonDataTemp)
                    logging.info(jsonDataTemp)

                # Move to next page    
                pageNumber = pageNumber + 1
                URL = 'https://www.darpa.mil/about-us/offices/tto/staff-list?PP=' + str(pageNumber)

            # if scrape was successful clear the database table and insert the new updated data
            logging.info("Clearing and Updating Database File")
            tto.truncate()
            tto.insert_multiple(full_data)

            tto_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            tto_lastupdated.insert({'lastupdated' : time})

        # if an error occurs return   
        except:
            logging.error("Error Scraping TTO Managers")
            return

        logging.info("TTO Managers Scrape Successful")


    # Function that scrapes all DSO managers from DARPA website
    def GetDSOProgramManagers(self, databaseTableName):
        dso = self.database.table(databaseTableName,cache_size=0) # init database table
        dso_lastupdated = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for dso
        pageNumber=0 # keeps track of page
        URL = 'https://www.darpa.mil/about-us/offices/dso/staff-list?PP=' + str(pageNumber) # Starting URL to get first page of DSO Program Managers
        full_data=[] # Holds results of scraper, list of JSON strings

        # Try Scraping, if error, abort mission
        try:

            while True:
                soup = self.returnSoupData(URL) # Get html data on page

                # find the dnn_ctr474_StaffList_dlProgramManagers id. This is a table that holds all the DSO managers. 
                # If the listingTable is not found, that means we have gone through all the pages and scraped all the DSO manager data, so we break out of the loop
                listingTable  = soup.find(id='dnn_ctr474_StaffList_dlProgramManagers')
                if(not listingTable):
                    break

                # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM
                managers = listingTable.find_all('div', class_='listing__right')
                # For every manager found on page
                for manager in managers:
                    interestList = []
                    programsList = []

                    name = manager.find('a') # Get the manager name
                    title = manager.find('div', class_='listing__position') # Get the managers title
                    description = manager.find('div', class_="listing__copy") # Get the managers description 
                    
                    # Get managers interests
                    interests = manager.find_all('a',class_='listing__tag-item listing__tag-link')
                    for interest in interests:
                        (interestList.append(interest.text))

                    # Go to the managers about page and pull program names that the manager is a part of
                    programSoup = self.returnSoupData(self.createAboutURL(name.text))
                    programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                    if(programs):
                        programNames = programs.find_all('div', class_='sidebar__link')
                        for programName in programNames:
                            programsList.append(programName.text)

                    # Store results in JSON Object and append to full data
                    jsonDataTemp = {
                        "name" : name.text,
                        "title" : title.text,
                        "description" : description.text,
                        "interests" : interestList,
                        "programs" : programsList
                    }
                    full_data.append(jsonDataTemp)
                    logging.info(jsonDataTemp)

                 # Move to next page    
                pageNumber = pageNumber + 1
                URL = 'https://www.darpa.mil/about-us/offices/dso/staff-list?PP=' + str(pageNumber)

            # if scrape was successful clear the database table and insert the new updated data
            logging.info("Clearing and Updating Database File")
            dso.truncate()
            dso.insert_multiple(full_data)

            
            dso_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            dso_lastupdated.insert({'lastupdated' : time})


        # if an error occurs return   
        except:
            logging.error("Error Scraping DSO Managers")
            return
        
        logging.info("DSO Managers Scrape Successful")


    # Function that scrapes all new program managers from DARPA website
    def GetNewProgramManagers(self, databaseTableName):

        new_program_managers = self.database.table(databaseTableName, cache_size = 0) # init database table
        new_program_managers_lastupdated  = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for new pms
        Listings = Query() # Query object 
        newPM = [] # Empty list to hold new updates to the new program managers page 
        full_data = [] # Holds results of scraper, list of JSON strings

    
        try:
            soup = self.returnSoupData('https://www.darpa.mil/work-with-us/new-program-managers') # Get html data

            # Find the dnn_ctr612_FeaturesFiltersList_dlMyItems id. This is a table that holds all the new program managers. 
            managerTable = soup.find(id='dnn_ctr612_FeaturesFiltersList_dlMyItems')
            # findall div elements within the table that have class listing_right. This narrows down where the actual manager information is stored in the DOM
            managers = managerTable.find_all('div', class_='listing__right')

            for manager in managers:
                interestList = []
                programsList = []

                name = manager.find('a') # Get the manager name
                office = manager.find('div', class_='listing__position') # Get the managers title
                description = manager.find('div', class_="listing__copy") # Get the managers description 

                # Get managers interests
                interests = manager.find_all('a',class_='listing__tag-item listing__tag-link')
                for interest in interests:
                    (interestList.append(interest.text))

                # Go to the managers about page and pull program names that the manager is a part of
                programSoup = self.returnSoupData(self.createAboutURL(name.text))
                programs = programSoup.find(id='dnn_ctr447_DispItemDetail_mySideBarType2_dlItems')
                if(programs):
                    programNames = programs.find_all('div', class_='sidebar__link')
                    for programName in programNames:
                        programsList.append(programName.text)
            
                # Store results in JSON Object 
                jsonDataTemp = {
                    "name" : name.text,
                    "office" : (office.text).split(", ")[1],
                    "description" : description.text,
                    "interests" : interestList,
                    "programs" : programsList
                }

                # Check if JSON Name field exists in the database file
                doesExistInDB = new_program_managers.contains( (Listings.name == jsonDataTemp['name']))
                # If it does not, it means that this JSON object new since the last run of this script
                if(not doesExistInDB):
                    logging.info("Adding " + jsonDataTemp['name'] + " to new data")
                    # Add the update to the newPM list, this list will be converted to an html table and attached to the daily update email
                    newPM.append(jsonDataTemp)
                else:
                    logging.info(jsonDataTemp['name'] + " already exists in database")
                
                # Add manager JSON object to full data list
                full_data.append(jsonDataTemp)
                logging.info(jsonDataTemp)

            # if scrape was successful clear the database table and insert the new updated data
            logging.info("Clearing and Updating Database File")
            new_program_managers.truncate()
            new_program_managers.insert_multiple(full_data)

            new_program_managers_lastupdated.truncate()
            now = datetime.now()
            time = now.strftime("%m/%d/%Y")
            new_program_managers_lastupdated.insert({'lastupdated' : time})

            # convert json updates to a html table 
            newPMHTMLTable = json2html.convert(json = newPM)

        except Exception as e:
            logging.error("Error Scraping New Program Managers")
            return "Error Occured while Scraping New Program Managers"

        logging.info("New Program Managers Scrape Successful")
        # Return html table
        return newPMHTMLTable





    # Function to compare dates. Used to figure out which darpa proposals are within 14 days, within 30 days, greater than 30 days
    def compareDates(self,currentResDate, currentDate):
        currentResDateFormatted = datetime.strptime(currentResDate, '%Y-%m-%d' )
        differenceDays = currentResDateFormatted - currentDate
        return differenceDays.days

    # Converts JSON date into a more readable date format
    def formatDate(self,date):
        date = date[:19]
        formattedDate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S' )
        return formattedDate

    # Each Darpa Listings have attachments or resourceID associated with it. In order to get that specific attachement, the resourceID of that attachement
    # is used. Therefore it need to get the resourceID. This function does that
    def getResourceIdOfPDF(self, _id, noticeID):

        # The resourceIDs of the attachment specified by its id are located at this url. The url contains json data
        url = 'https://beta.sam.gov/api/prod/opps/v3/opportunities/' + _id + '/resources'
        resourcesForListing = json.loads(self.getRequest(url).data) # Load json data from the get request to the url

        dateToResourceIDMap = {} # Map date to the resource ID. We eventually want the most recent resource ID
        resourceID = '' # init a resource ID variable

        # For every attachment linked to the posting
        for i in range(len(resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'])):
            # if the attachement exists and its not deleted
            if( resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['fileExists'] == "1" and 
                resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['deletedFlag'] == "0" ):
                try:
                    # if noticeId is in the attachement name, if track changes is not in the atttachement name, and if the attachement is a pdf
                    # in some cases and attachement might not have a name field so this might throw and error. Encapsulate in a try except and continue if execption occurs
                    if(noticeID in resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['name'] and
                        'track' not in resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['name'].lower() and
                        resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['name'][-3:] == 'pdf' ):

                        # We want to get the most recent attachement so save the posted date of the attachment, map the date posted to the resource id
                        dateString = (resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['postedDate'])
                        dateToResourceIDMap.update({        self.formatDate(dateString)  :   resourcesForListing['_embedded']['opportunityAttachmentList'][0]['attachments'][i]['resourceId']   })
                except Exception as e:
                    #print("Execption in getResourceIDofPDF")
                    #print(e)
                    continue
        # Sort the dateToResourceIDMap the last key value pair is the most recent document of interest          
        od = collections.OrderedDict(sorted(dateToResourceIDMap.items()))
        # If there is nothing in the dict return none
        if(not (od) ):
            return None
        
        # Get the last value of the dictionary since this is the most recent resourceID of the document of interest
        lastValue = od.popitem()  
        resourceID = lastValue[1]

        return resourceID
    
    def formatForEmail(self,data):
        del data['noticeid']
        del data['lastupdateddate']
        del data['lastpublisheddate']
        del data['url']
        del data['awardee']
        del data['contractValue']
        del data['color']
        del data['importantDates']

        data['Contract Name'] = data.pop('contractname')
        data['Proposal Due Date'] = data.pop('proposalduedate')
        data['Type'] = data.pop('type')
        #jsonData['Important Info'] = jsonData.pop('importantDates')

        return data

    # Function to scrape Darpa listings from beta.sam.gov
    def GetDarpaListings(self,databaseTableName):

        darpaListings = self.database.table(databaseTableName,cache_size=0) # init database table for darpaListings
        darpa_listings_lastupdated  = self.database.table(databaseTableName+"_lastupdated", cache_size=0) # init database lastupdated table for new pms
        newDarpa = [] # List for new entries
        newUpdates = [] # List of new updates
        Listings = Query()

        # URL for getting listings, returns JSON information. Faster than scraping website itself since JSON is quicker to parse than HTML 
        URL = 'https://beta.sam.gov/api/prod/sgs/v1/search/?random=1586481779318&index=opp&q=&page=0&sort=-modifiedDate&mode=search&is_active=true&organization_id=300000412'
    
        # Get request to get first page of darpa listings - JSON format
        data = json.loads(self.getRequest(URL).data)

        # Odds are there will be multiple pages of data we must visit to get all the DARPA listings. Thankfully, the json data returned from the GET requests contains the amount of pages in total 
        # so that number is saved 
        numberOfPages = int(data['page']['totalPages'])
        full_data = [] # Will contain all the data that will be passed through the api to be displayed in the table on the front end

        # Handling pagination, iterate through each page
        for i in range(numberOfPages):
            # Get the URL for the page by modifiying the page parameter in the url
            urlOfInterest  = 'https://beta.sam.gov/api/prod/sgs/v1/search/?random=1586481779318&index=opp&q=&page='+ str(i) + '&sort=-modifiedDate&mode=search&is_active=true&organization_id=300000412'

            # Get request for next page of darpa listings
            pageData = json.loads(self.getRequest(urlOfInterest).data)

            # Get the number of records per page
            numberOfRecords = int(pageData['page']['size'])
            
            # Iterate through each record on the page
            for j in range(numberOfRecords):

                # Extract Data that is needed by parsing the JSON returned from the page URL    
                awardee = None
                contractValue = None
                importantInformation = None
                color = 'None'
                _id = (pageData['_embedded']['results'][j]['_id'])
                url = 'https://beta.sam.gov/opp/' + _id +'/view'
                currentResponseDate = (str(pageData['_embedded']['results'][j]['responseDate']).split('T'))[0]
                lastUpdatedDate = (str(pageData['_embedded']['results'][j]['modifiedDate']).split('T'))[0]
                lastPublishedDate =  (str(pageData['_embedded']['results'][j]['publishDate']).split('T'))[0]
                contractName  = pageData['_embedded']['results'][j]['title']
                noticeID = pageData['_embedded']['results'][j]['solicitationNumber']
                postingType = pageData['_embedded']['results'][j]['type']['value']

                if(currentResponseDate != 'None'):
                    if(self.compareDates(currentResponseDate, datetime.now()) <= -2):
                        continue # Disregard listings that are in the past by more than two days
                    elif(self.compareDates(currentResponseDate, datetime.now()) <= 14):
                        color = 'red' # Listings that are within 14 days of proposal due date will be shaded red
                    elif(self.compareDates(currentResponseDate, datetime.now()) <= 30):
                        color = 'yellow' # Listings that are within 30 days of proposal due date will be shaded yellow
                    elif(self.compareDates(currentResponseDate, datetime.now()) > 30):
                        color = 'green' # Listings that are greater than 30 days of proposal due date will be shaded green
                                
                # If the record is of type Award Notice, pull the awardee and the contract value, this information is on a different URL so a new get request is needed per Award Notice record
                if(postingType=="Award Notice"):
                    awardURL = 'https://beta.sam.gov/api/prod/opps/v2/opportunities/' + _id
                    awardData = json.loads(self.getRequest(awardURL).data)
                    awardee = awardData['data']['award']['awardee']['name']
                    contractValue = awardData['data']['award']['amount']
                
                # Get PDF of BAA
                if(postingType=="Presolicitation"):
                    # Get resource ID of pdf 
                    resourceID = self.getResourceIdOfPDF(_id, noticeID)
                    #print(resourceID)

                    # If a valid resourceID is returned
                    if(resourceID):
                        # The actual pdf is located on another URL so a get request is made
                        getPDFUrl = 'https://beta.sam.gov/api/prod/opps/v3/opportunities/resources/files/' + resourceID + '/download?api_key=null&token='
                        pdfRaw = self.getRequestPDF(getPDFUrl)
                        pdf = io.BytesIO(pdfRaw.data)

                        try:
                            read_pdf = PyPDF2.PdfFileReader(pdf) # PDF reader object

                            # Loop through the first 10 pages to find the important dates/info. Usually this information is found within the first 10 pages
                            for i in range(10):
                                # Extract Text from page
                                content = (read_pdf.getPage(i).extractText())
                                # If the current page is the Table of Contents, continue on to the next page
                                isTOC = re.search(r"[Cc][Oo][Nn][Tt][Ee][Nn][Tt][Ss]",content)
                                if(isTOC):
                                    continue
                                # Search for "Overview Information" on the page. If the creator of the pdf follows the right DARPA listings pdf format, all important dates and information is listed on this page
                                partIPageNumber = re.search(r"[Oo][Vv][Ee][Rr][Vv][Ii][Ee][Ww]\s+[Ii][Nn][Ff][Oo][Rr][Mm][Aa][Tt][Ii][Oo][Nn]", content)
                                # If the page is found extract the content 
                                if(partIPageNumber):
                                    content = content.replace('\n', ' ')
                                    content = ' '.join(content.split())
                                    importantInformation = content
                                    break
                        except:
                            pass
                            #print("Exeption Occured")
                        pdfRaw.release_conn()
    
                # Store listing information in a json object    
                jsonDataTemp =  {

                                "contractname"          :   contractName,
                                "noticeid"              :   noticeID,
                                "proposalduedate"       :   currentResponseDate,
                                "lastupdateddate"       :   lastUpdatedDate,
                                "lastpublisheddate"     :   lastPublishedDate,
                                "type"                  :   postingType,
                                "url"                   :   url,
                                "awardee"               :   awardee,
                                "contractValue"         :   contractValue,
                                "color"                 :   color,
                                "importantDates"        :   importantInformation
                                }

                # Check to see if listings is already in the database
                doesExistInDB  = darpaListings.contains( (Listings.contractname == jsonDataTemp['contractname'] ))
                # If not, add the Listing JSON Object to the newDarpa list
                if(not doesExistInDB):
                    logging.info(jsonDataTemp['contractname'] + " is a new listing")
                    temp = copy.deepcopy(jsonDataTemp)
                    jsonForEmail = self.formatForEmail(temp)
                    newDarpa.append(jsonForEmail)

                # If the listing already exists in the database, check to see if it has been updated
                else:
                    if(jsonDataTemp['type'] != "Award Notice"):
                        entries = darpaListings.search(Listings.contractname == jsonDataTemp['contractname'])
                        for entry in entries:
                            if(entry['noticeid'] == jsonDataTemp['noticeid']):
                                if( entry['lastupdateddate'] != jsonDataTemp['lastupdateddate']  ):
                                    logging.info(jsonDataTemp['contractname'] + " is an updated listing")
                                    # If the listing has been updated since last run, add the Listing JSON object to the newUpdate List
                                    temp = copy.deepcopy(jsonDataTemp)
                                    jsonForEmail = self.formatForEmail(temp)
                                    newUpdates.append(jsonForEmail)

                # Append JSON obects for each record together to form the full data. 
                logging.info(jsonDataTemp)
                full_data.append(jsonDataTemp)
        
        # Delete all old entries from database table
        darpaListings.truncate()

        # Insert most recent entries into database
        darpaListings.insert_multiple(full_data)

        # Update the lastupdated date to reflect the date of the last sucessful scraper run
        darpa_listings_lastupdated.truncate()
        now = datetime.now()
        time = now.strftime("%m/%d/%Y")
        darpa_listings_lastupdated.insert({'lastupdated' : time})
        
        logging.info("New Listings")
        logging.info(newDarpa)

        logging.info("New Updates")
        logging.info(newUpdates)

        # Queries to group listings based on color or days till proposal due date
        green = darpaListings.search(Listings.color == 'green')
        yellow = darpaListings.search(Listings.color == 'yellow')
        red = darpaListings.search(Listings.color == 'red')

        # Convert json to html table so results can be sent via an email
        newDarpaListingsTable = json2html.convert(json=newDarpa)
        updatedDarpaListingsTable = json2html.convert(json=newUpdates)
        redTable= json2html.convert(json = red)
        yellowTable= json2html.convert(json = yellow)
        greenTable= json2html.convert(json = green)

        # Return full_data 
        logging.info("DARPA Listings Scrape Sucessful")

        return newDarpaListingsTable, updatedDarpaListingsTable, redTable, yellowTable, greenTable

    # Function to send email containing results from the last run of the scraper
    def generateEmailBody(self, newDarpaListingsTable, updatedDarpaListingsTable, redTable, yellowTable, greenTable, newPMHTMLTable):
        logging.info("Generating Automated Email Body.....")
        # load the email template
        with open("emailTemplate.html") as inf:
            txt = inf.read()
            soup = BeautifulSoup(txt,features="html.parser")

        # Use beautiful soup to find elements in the emailTemplate file
        newDarpaListings = soup.find(class_="NewDarpaListingsText")
        updatedDarpaListings = soup.find(class_="UpdatedDarpaListingsText")
        #lessThan14 = soup.find(class_="Darpa_less_than_14")
        #between14and30 = soup.find(class_="Darpa_between_14_and_30")
        #greaterThan30 = soup.find(class_="Darpa_greater_than_30")
        newPMListings = soup.find(class_='NewProgramManagersText')

        # Insert the tables after the elements found above
        newDarpaListings.insert_after(newDarpaListingsTable)
        updatedDarpaListings.insert_after(updatedDarpaListingsTable)
        #lessThan14.insert_after(redTable)
        #between14and30.insert_after(yellowTable)
        #greaterThan30.insert_after(greenTable)
        newPMListings.insert_after(newPMHTMLTable)

        # Convert to html
        soup = html.unescape(str(soup))

        with open("automatedEmail.html", "w", encoding='utf-8') as file:
            file.write(str(soup))

        logging.info("Automated Email Body Sucessfully Generated")

            


db = TinyDB('DARPA.json')
scraper = DARPAScraper(db)


scraper.GetMTOProgramManagers('mto')

scraper.GetI2OProgramManagers('i2o')

scraper.GetBTOProgramManagers('bto')

scraper.GetSTOProgramManagers('sto')

scraper.GetTTOProgramManagers('tto')

scraper.GetDSOProgramManagers('dso')

newDarpaListingsTable, updatedDarpaListingsTable, redTable, yellowTable, greenTable = scraper.GetDarpaListings('darpa_listings')

newPMHTMLTable = scraper.GetNewProgramManagers('new_program_managers')

scraper.generateEmailBody(newDarpaListingsTable,updatedDarpaListingsTable,redTable,yellowTable,greenTable,newPMHTMLTable)