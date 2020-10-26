
"""
Created on Sat Oct 24 18:37:10 2020

@author: Bryan Smith
"""

import Skyhoundz as skypy
import pandas as pd


'''
This program will get all data from the skyhoundz website 
utilizing the Skyhoundz.py file
All data can be scraped by selecteing the correct event wanted,
data will be stored in csv file located at outpath location
'''
outpath ='C:/Users/smith/Documents/GitHub/DIODE/Discdogathonresults.csv'
url = "https://skyhoundz.com/previous-competition-results/"

#event_wanted = 'skyhoundz-classic-results'
#event_wanted = 'xtreme-distance-results'
event_wanted = 'discdogathon-results'

classic = skypy.Classic_WebScrape(url, event_wanted)
classic.to_csv(outpath)





