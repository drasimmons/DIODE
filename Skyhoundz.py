# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 12:47:13 2020

@author: Bryan Smith
@author: Amber Simmons*

*Amber Simmons' XtremeWebScrapeFunctions.py as been added to this file
so that all functions for gathering skyhoundz data can be found here

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


# this function scrapes all table data from webpage

def get_data(html):
    data = []
    with urlopen(html) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        rows = soup.find_all('tr') #Find all table row tags
        for row in rows: #For each row in that tag
            cols = row.find_all('td') #Find all the columns
            cols = [ele.text.strip() for ele in cols]  #Trim the junk off the cols
            data.append([ele if ele else '' for ele in cols])   #Append while ignoring empty vals
    return data


# this function organizes the data from the get_data function
def parse_data(data):
    titles = []
    tables = {}
    for row in data:
        if len(row) == 1:
            current_title = row[0]
            tables[current_title] = []
            titles.append(current_title)
        elif len(row) != 0:
            tables[current_title].append(row)
    return(titles, tables)


# this function places all subtables on a results page into one large table
def get_pandas(titles_in, tables_in):
    for j in range(len(tables_in)):
        for i in range(len(tables_in[titles_in[j]])):
            desc = titles_in[j].split(" / ")
            for string in desc:
                tables_in[titles_in[j]][i].append(string)
        if j==0:
            t = pd.DataFrame(tables_in[titles_in[j]],
                              columns=['Placement','Team','Score','TitleEligibile','Year','Event','Date','Division'])
        else:
            t = t.append(pd.DataFrame(tables_in[titles_in[j]],
                       columns=['Placement','Team','Score','TitleEligibile',
                                'Year','Event','Date','Division']))
    return t


# this function pulls all Xtreme Distance data from Skyhoundz website

def XtremeDist_WebScrape():
    # let's grab html from page listing links to individual year results
    html_outer = urlopen("https://skyhoundz.com/previous-competition-results/")

    # turn it to soup
    soup_outer = BeautifulSoup(html_outer,'html.parser')

    # gather each link containing xtreme distance results
    result_links = []
    for a in soup_outer.find_all('a'):
        if re.search('xtreme-distance-results',a['href']):
            result_links.append(a['href'])

    # the following loop cycles through each url containing results (1 page per year of results)
    # and creates pandas dataframe of all results combined
    for k in range(len(result_links)):

        html_inner = urlopen(result_links[k])
        soup_inner = BeautifulSoup(html_inner,'html.parser')

        data = get_data(result_links[k])
        titles, tables = parse_data(data)

        if k == 0:
            p = get_pandas(titles, tables)
        else:
            p = p.append(get_pandas(titles, tables))

    return p



'''This Function will scrape all of the skyhounds classic
results. It takes in a string, which is the link to the skyhoundz
results page, and returns a df for DiscDogathon, Classic, or
Extreme Distance based on event argument.

***NOTE***
This function has now been genralized to take in other events
Function has second argument event which can be one of the following strings:
    skyhoundz-classic-results
    xtreme-distance-results
    discdogathon-results
    
10/24/20 Still need to add error handling for event!= allowed event    
'''
def Classic_WebScrape(classic_link, event):
    # let's grab html from page listing links to individual year results
    html_outer = urlopen(classic_link)

    # turn it to soup
    soup_outer = BeautifulSoup(html_outer,'html.parser')

    # view it
    #print(soup_outer.prettify())

    # store each link that connects to a page of xtreme distance results
    result_links = []

    #event = 'skyhoundz-classic-results'


    for a in soup_outer.find_all('a'):
        if re.search(event,a['href']):
            result_links.append(a['href'])
 
#From here you need to open all links, get all tables for each
#link and combine all event type into single df, then single files           
            
    #Each link if for a different year, so lets store each years
    #dataframe in a list of dataframs
    year_dfs=[]
    
    for j in range(len(result_links)):
        year_link = result_links[j]
       
        temp_df = dataframe_from_tables(year_link)
        print(year_link)
        year_dfs.append(temp_df)
        
    df_all_years = pd.concat(year_dfs)
    return df_all_years
            

'''This function takes in an html link and returns a dataframe
containing all tables
'''
def dataframe_from_tables(link):
    
    #Reads html and stores data in a list of dataframes
    dfs = pd.read_html(link, header=0)
    dfs_fixed=[]
    year=''
    
    #Loop through data frames to correct first row, add columns
    for x in range(len(dfs)):
        temp = dfs[x]
        tname = temp.columns[0]
        print(tname)
        #year, event, location, mm,dd,yy,evtype=tname.split('/')
        
        tsplit = tname.split('/')
        
        if len(tsplit)>6:
            year = tsplit[0]
            event = tsplit[1]
            location = tsplit[2]
            mm = tsplit[3]
            dd = tsplit[4]
            yy = tsplit[5]
            evtype = tsplit[6]
        
            temp.columns=temp.iloc[0]
            temp2 = temp.drop(0)
        
            temp2['Year']=year
            temp2['Event']=event
            temp2['Location']=location
            temp2['MM']=mm
            temp2['DD']=dd
            temp2['YYYY']=yy
            temp2['Event_Type']=evtype
        
        
        #Xtreme Distance and DiscDogathon table headers have 
        #less arguments, this is to address those and make
        #Classic_Webscrape function work for all game types, instead of needing other 
        #functions
        elif len(tsplit)==6:
            year = tsplit[0]
            location = tsplit[1]
            mm = tsplit[2]
            dd = tsplit[3]
            yy = tsplit[4]
            evtype = tsplit[5]
        
            temp.columns=temp.iloc[0]
            temp2 = temp.drop(0)
        
            temp2['Year']=year
            
            temp2['Location']=location
            temp2['MM']=mm
            temp2['DD']=dd
            temp2['YYYY']=yy
            temp2['Event_Type']=evtype
            
      
        dfs_fixed.append(temp2)
        
    
    '''
    ****************NOTE********************
    the following if statement is a work around for the difference
    of the format that occures in 2009. A fix for this issue is still
    in development
    
    
    ''''
    if int(year) > 2009:
        result = pd.concat(dfs_fixed)
        return result
    else:
        return


    
        
        



    





