# -*- coding: utf-8 -*-
"""Debateorg Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14Kv_fPDxbr2zoZPy_mzTR9UBg-lH9HZ8

# **Arguments, Votes, User Information Scraper for Debate.org**

# *Shilong Wang, Sungbin Youk, & René Weber**

# *Media Neuroscience Lab - UC Santa Barbara*

*A special acknowledgment and thank you to research assistant Shilong who foremost developed this notebook as part of a summer project in 2021 with the supervision of Sungbin Youk and René Weber.

#Introduction

Welcome to the Python Google Colab Notebook for scraping arguments, votes, and user information from [Debate.org](https://www.debate.org/)! This notebook was created by Shilong Wang along with the supervision and guidance from the Media Neuroscience Lab at UCSB to introduce webscraping to social science researchers . 

This notebook collects various information from debates that are in post-voting status. Specifically, there are three types of information that are scraped. First, information about debates  includes the title of the debate, the user name of the winner, the start date of the debate, number of comments and more. Second, the arugment information includes the number of rounds and the arguments made in each round. Third, information about the user is also collected. The output is stored in either csv or pickle files. 

Specifically, this notebook has three main sections: first, setting up the output directory on Google Drive; second, preparing the environment; third, running the code (there are 5 parts of the code, each with a different purpose). For each section, there is detailed instruction. Please follow the guidelines in these three sections in order as each step builds on the previous one.

Disclaimer: This code may automatically ignore a few debates when encountering errors of any sort. However, please rest assured that the amount of such circumstances will be very small and will not influence the overall accuracy of the data.

# **Important:** Setting up the output directory on Google Drive

Please do the following before running the code below to ensure that the code functions properly and that all of the files and data are loaded and stored on your Google Drive successfully.

1. Go to your Google drive by clicking the link below: https://accounts.google.com/signout/chrome/landing?continue=https://drive.google.com/drive/

2. Go to "My Drive" at the top-left corner of the screen

3. Create a folder and name it "Debate_Webscraper" (please create a folder with exactly the same name as this)

4. Check once again if the folder, "Debate_Webscraper," exists under "My Drive" before you run the following code, in order to ensure the following code runs properly.

5. You are all set and may start exploring this notebook. Please keep in mind that you need to run the code in order just so the code would not run into errors because a later section may need to read the file generated in an earlier section.

# Preparing the environment

## Mounting to Google Drive
"""

# Mounting the Google Drive 
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# Commented out IPython magic to ensure Python compatibility.
# Change directory to our project folder 
# %cd /content/drive/MyDrive/Debate_Webscraper

"""## Importing packages"""

# Import csv and pandas to write to csv:
import csv 
import pandas as pd

# Import the 'Requests' library to make HTTP requests:
import requests

# Import BeautifulSoup for RegEx
from bs4 import BeautifulSoup
import re
import urllib.request

# Import Pickle to store the output file
import pickle

# To check if file exists
import os

# To add delays
import time

"""# 1- Collecting general information about debates

This section is deisgned to collect the overarching information about debates. 

The output file from this section will be named "debates_url.csv," a CSV file storing information like the titles, URLs, number of rounds, number of votes, and number of comments of each debate. 

Notice: our code has the potential to collect as many debates as you want. For demonstration purposes, the following code only collects debates on the first four pages. However, you may collect more by simply change the the number in the code:  `for i in range(1,5)`. `range(1,n)` means you will collect page 1 to page n-1).
"""

def write_page_to_file(input_url):
  # Define the URL:
  print("I'm trying to access page "+ input_url)
  response= urllib.request.urlopen(input_url)

  soup = BeautifulSoup(response)


  # Find all content surrounded by the tab "h3" because the titles are in them
  all_h3 = soup.find_all('h3')

  # Find titles and append them as a list
  titles= []
  for h3 in all_h3:
      titles.append(h3.getText())


  # Find all content surrounded by the tab "a" because the links are in them
  all_a = []
  for h3 in all_h3:
      all_a.append(h3.find('a'))

  # find the links and print them out in a standart web format
  all_link = ["https://www.debate.org" + a.get("href") for a in all_a]
  all_link


  # going into each of the debate on page 1
  source_pages = [BeautifulSoup(urllib.request.urlopen(link)) for link in all_link]


  no_rounds = []
  for source_page in source_pages:
    tab_0_content = source_page.find_all(id="tab0")
    no_rounds.append(tab_0_content[0].getText())
  no_rounds


  no_comments = []
  for source_page in source_pages:
    tab_1_content = source_page.find_all(id="tab1")
    no_comments.append(tab_1_content[0].getText())
  no_comments


  no_votes = []
  for source_page in source_pages:
    tab_2_content = source_page.find_all(id="tab2")
    no_votes.append(tab_2_content[0].getText())


  # append data to list
  rows = zip(titles,all_link,no_rounds,no_votes,no_comments)

  # Looking for the minimum number of votes for the scraped debates
  for votes in no_votes:
    vote = votes.replace("Votes (","").replace(")","")
  return int(vote), rows

url = 'https://www.debate.org/debates/?post=true&page=1&order=4&sort=1'


url_list = []
used_url_list = []

for i in range(1,5):
    string_to_replace = 'page=' + str(i)
    result_str = url.replace('page=1', string_to_replace)
    url_list.append(result_str)
print("We will be scraping debates and their urls from pages 1 to {}".format(len(url_list)))


# Setting the minimum number of votes
target_min_vote = 0

with open("debates_url.csv", 'a') as f:
  writer = csv.writer(f)
  writer.writerow(['title', 'url','no_rounds','no_votes', 'no_comments'])
  for link in url_list:
    time.sleep(1)
    if link not in used_url_list:
      try:
        min_vote, rows = write_page_to_file(link)
        for row in rows:
          writer.writerow(row)
        if min_vote < target_min_vote:
          print("The debae scraper stopped as the number of votes are less than {}".format(target_min_vote))
          break
        used_url_list.append(link)
      except Exception as e:
        print(e)
        time.sleep(60)

  print("Finished running scripts")
print(pd.read_csv("debates_url.csv").head())

"""# 2- Collecting detailed information about the debate

This section scrapes detailed debate information for each debate 

The output file from this section will be named "debates_url_info.csv," a CSV file storing information like the username for the instigator and contender, the voting style, the started date, updated date, and viewed times.
"""

def write_page_to_file(input_url):
  print("storing debate information for {}".format(input_url))

  # dictionary to store detailed information about debates
  debate_info = {}

  # getting the source page of the debate
  response= urllib.request.urlopen(input_url)
  source_page = BeautifulSoup(response)

  #scraping detailed info about debates
  debate_info['debate_winner'] = source_page.find("div", class_= "winner").getText()
  debate_info['voting_style'] = source_page.find_all("td", class_= "c2")[0].getText()
  debate_info['started_date'] = source_page.find_all("td", class_= "c2")[2].getText()
  debate_info['updated'] = source_page.find_all("td", class_= "c2")[3].getText()

  viewed_original = source_page.find_all("td", class_= "c2")[4].getText()
  debate_info['viewed']= viewed_original.replace("times", "")

  debate_info['point_system'] = source_page.find_all("td", class_= "c2")[1].getText()
  debate_info['category'] = source_page.find_all("td", class_= "c4")[0].getText()
  
  status_code = source_page.find("div", {"id": "info"})
  debate_info['status'] = status_code.findAll('div')[0].getText()
      
  # the instigator
  #getting the names, side, and points
  instigator_code = source_page.find("div", {"id": "instigatorWrap"})
  debate_info['instigator_name'] = instigator_code.find('div', class_ = "un").getText()
  debate_info['instigator_side'] = instigator_code.find('span').getText()
  
  instigator_code_edited = instigator_code.find('div', class_ = "pointsCount").getText()
  debate_info['instigator_points'] = instigator_code_edited.replace("Points","")

  #the contender
  #getting the names, side, and points
  contender_code = source_page.find("div", {"id": "contenderWrap"})
  debate_info['contender_name'] = contender_code.find('div', class_ = "un").getText()
  debate_info['contender_side'] = contender_code.find('span').getText()
  
  contender_code_edited = contender_code.find('div', class_ = "pointsCount").getText()
  debate_info['contender_points'] = contender_code_edited.replace("Points","")

  return debate_info

df = pd.read_csv('debates_url.csv')


used_url_list = []

for index, row in df.iterrows():
  if row['url'] not in used_url_list:
    try:
      debate_info = write_page_to_file(row['url'])
      for key in debate_info.keys():
        df.loc[index, key] = debate_info[key]
      used_url_list.append(row['url'])
    except Exception as e:
      print(e)
      time.sleep(60)
  else:
    print("{} is already saved".format(row['url']))

print(pd.read_csv("debates_url.csv").head())
df.to_csv('debates_url_info.csv')

"""# 3-Collecting arguments from debates 

This section will produce a .pkl (Python built-in dictionary) file, named "argument_text.pkl" collecting the arguments (texts) of each debate . All of the texts in each round of a debate from both the instigator and the contender are stored in this dictionary.


"""

def write_debate_to_file(input_url):
  print("I'm trying to access page "+ input_url)
  response= urllib.request.urlopen(input_url)
  soup = BeautifulSoup(response)

  # Getting the arguments in the debate
  rounds = soup.find('table', {'id':"rounds"})
  # Getting the arguments in each round
  round = rounds.find_all('tr')
  
  # Iterating over each round and storing the data in dictionary
  arguments_dict = {}
  count = 1
  for each_round in round: 
    # Getting the arguments for each stance
    argument_text = each_round.find_all('div', {'class':"round-inner"})
    arguments_dict_each_round = {}
    for i in argument_text:
      text = i.getText()
      #Getting the stance
      if "\nPro\n" in text:
        stance = "Pro"
        text = text.replace("\nPro\n","")
      elif "\nCon\n" in text:
        stance = "Con"
        text = text.replace("\nCon\n","")
      # Cleaning the text
      text = text.replace("\n","")
      text = text.replace("\r","")
      text = text.replace("Report this Argument","")

      #Saving to a dictionary
      arguments_dict_each_round[stance] = text
    # Compiling the dictionary across rounds
    arguments_dict[count] = arguments_dict_each_round
    count += 1
  
  print("Successfully stored {} rounds of arguments".format(len(arguments_dict)))
  return arguments_dict

debates = {}
df = pd.read_csv('debates_url.csv')

used_url_list = []

for index,row in df.iterrows():
  if row['url'] not in used_url_list:
    try:
      debate_url = row['url']
      debates[debate_url] = write_debate_to_file(debate_url)
      used_url_list.append(row['url'])
    except Exception as e:
      print(e)
      time.sleep(60)
  else:
    print("{} is already saved".format(row['url']))

# Storing the arguments as pkl files
with open('argument_text.pkl', 'wb') as f:
    pickle.dump(debates, f)

# Checking to see if the pickled file works
# load
with open('argument_text.pkl', 'rb') as f:
    checking = pickle.load(f)
if len(checking) == len(debates):
  print("The storing is successful")

"""# 4-Collecting rating information

This section will produce a .pkl file, named "ratings_information.pkl," collecting the information under "Votes" in debate.org. The information includes the user ID of the rater (i.e. voter) and their preferences toward the six choices pending to rate.
"""

def get_page_dic(input_url):
  print("I'm trying to access page "+ input_url)
  response= urllib.request.urlopen(input_url)
  source_page = BeautifulSoup(response)

  #getting the page title
  page_title = source_page.find('h1', class_="top").text

  #getting the voting numbers 
  no_votes = source_page.find_all(id="tab2")
  vt_str = no_votes[0].getText()
  vt_num = vt_str[vt_str.index("(") + 1:vt_str.rindex(")")]

  #getting the voters info
  ## calculating number of pages for voters
  page_number = int(vt_num)//10
  if int(vt_num)%10 != 0:
    page_number = page_number + 1
    print("there are {} pages regarding vote information".format(page_number))
  ## getting voter's id and ratings
  voter_dic = {}
  for i in range(1,page_number +1):
    voter_dic = get_rating(input_url+"votes/{}/".format(i), voter_dic)

  page_content_dic = dict({'Debate_name':page_title, 'Vote_number': int(vt_num), 'Voter':voter_dic})
  return {input_url:page_content_dic}

def get_rating(input_url,voter_dic):
  print("I'm trying to access {}".format(input_url))
  response= urllib.request.urlopen(input_url)
  source_page = BeautifulSoup(response)
  
  # Each voter's rating information
  for table in source_page.find_all('div', {'class': 'vote'}):
    # getting voter ID
    try:
      rater_id = table.find('div',class_='ago').find('a').text
    except:
      rater_id = table.find('div',class_='ago').find('strong').text
    print(rater_id)
    # getting IDs of debaters
    debater_id = []
    for i in table.find_all('tr')[0].find_all('th', {'class': 'a'}):
      debater_id.append(i.text)
    # gettig the votes by iterating each row
    vote_info = {}
    for row in table.find_all('tr')[1:-1]:
      vote_category = row.find('td', class_='a').text.replace(":","")
      rating_name = get_rating_name(debater_id, row.find_all('td')[1:-1])
      vote_info[vote_category] = rating_name
    voter_dic[rater_id]= vote_info
  return voter_dic

def get_rating_name(debater_id, row):
  ratings = [len(x.text) for x in row]
  location = ratings.index(0)
  name = debater_id[location]
  return name

debates = {}
df = pd.read_csv('debates_url.csv')

used_url_list = []

for index,row in df.iterrows():
  if row['url'] not in used_url_list:
    try:
      debate_url = row['url']
      debates[debate_url] = get_page_dic(debate_url)
      used_url_list.append(row['url'])
    except Exception as e:
      print(e)
      time.sleep(60)
  else:
    print("{} is already saved".format(row['url']))

# Storing the ratings information  as pkl files
with open('ratings_information.pkl', 'wb') as f:
    pickle.dump(debates, f)

# Checking to see if the pickled file works
# load
with open('ratings_information.pkl', 'rb') as f:
    checking = pickle.load(f)
if len(checking) == len(debates):
  print("The storing is successful")

"""# 5- Collecting voters' information

This section creates a list of user ID (under "voters_id.pkl") for the voters obtained from the previous section. The main outout file will be named "user_information.pkl," collecting information about the user (e.g., their relationship status, ethnicity, and ideology).
"""

#function to collect tables of users' information
def write_user_page_to_file(input_url):
    print("storing user information for {}".format(input_url))

    # getting the source page
    response= urllib.request.urlopen(input_url)
    source_page = BeautifulSoup(response)
    #Creating the overarching dictionary
    All_tables = {}
    
    #personal info table
    try:
      person_info_table = {}

      for td in source_page.find_all("div", id= "info"):
          Online = td.find_all("td", class_="c2")[0].text.replace("-",'')
      person_info_table['Online'] = Online

      for td in source_page.find_all("div", id= "info"):
          Updated = td.find_all("td", class_="c2")[1].text.replace("-",'')
      person_info_table['Updated'] = Updated

      for td in source_page.find_all("div", id= "info"):
          Joined = td.find_all("td", class_="c2")[2].text.replace("-",'')
      person_info_table['Joined'] = Joined

      for td in source_page.find_all("div", id= "info"):
          President = td.find_all("td", class_="c2")[3].text.replace("-",'')
      person_info_table['President'] = President

      for td in source_page.find_all("div", id= "info"):
          Ideology = td.find_all("td", class_="c2")[4].text.replace("-",'')
      person_info_table['Ideology'] = Ideology

      for td in source_page.find_all("div", id= "info"):
          Party = td.find_all("td", class_="c2")[5].text.replace("-",'')
      person_info_table['Party'] = Party

      for td in source_page.find_all("div", id= "info"):
          Relationship = td.find_all("td", class_="c2")[6].text.replace("-",'')
      person_info_table['Relationship'] = Relationship

      for td in source_page.find_all("div", id= "info"):
          Interested = td.find_all("td", class_="c2")[7].text.replace("-",'')
      person_info_table['Interested'] = Interested

      for td in source_page.find_all("div", id= "info"):
          Looking = td.find_all("td", class_="c2")[8].text.replace("-",'')
      person_info_table['Looking'] = Looking

      for td in source_page.find_all("div", id= "info"):
          Name = td.find_all("td", class_="c5")[0].text.replace("-",'')
      person_info_table['Name'] = Name

      for td in source_page.find_all("div", id= "info"):
          Gender = td.find_all("td", class_="c5")[1].text.replace("-",'')
      person_info_table['Gender'] = Gender

      for td in source_page.find_all("div", id= "info"):
          Birthday = td.find_all("td", class_="c5")[2].text.replace("-",'')
      person_info_table['Birthday'] = Birthday

      for td in source_page.find_all("div", id= "info"):
          Email = td.find_all("td", class_="c5")[3].text.replace("-",'')
      person_info_table['Email'] = Email

      for td in source_page.find_all("div", id= "info"):
          Education = td.find_all("td", class_="c5")[4].text.replace("-",'')
      person_info_table['Education'] = Education

      for td in source_page.find_all("div", id= "info"):
          Ethnicity = td.find_all("td", class_="c5")[5].text.replace("-",'')
      person_info_table['Ethnicity'] = Ethnicity

      for td in source_page.find_all("div", id= "info"):
          Income = td.find_all("td", class_="c5")[6].text.replace("-",'')
      person_info_table['Income'] = Income

      for td in source_page.find_all("div", id= "info"):
          Occupation = td.find_all("td", class_="c5")[7].text.replace("-",'')
      person_info_table['Occupation'] = Occupation

      for td in source_page.find_all("div", id= "info"):
          Religion = td.find_all("td", class_="c5")[8].text
      person_info_table['Religion'] = Religion
    except:
      pass

    #debate stats table
    debate_stats = {}

    source_page2 = source_page.find_all('table')     
    for n in source_page2:
      if n.find('tr').text == 'Debate Statistics':
        source_page2 = n
        break

    debate_stats['Debates'] = source_page2.find_all('td', class_="right")[0].text
    debate_stats['Lost'] = source_page2.find_all('td', class_="right")[1].text
    debate_stats['Tied'] = source_page2.find_all('td', class_="right")[2].text
    debate_stats['Won'] = source_page2.find_all('td', class_="right")[3].text
    debate_stats['Win Ratio'] = source_page2.find_all('td', class_="right")[4].text
    debate_stats['Percentile'] = source_page2.find_all('td', class_="right")[5].text
    debate_stats['Elo Ranking'] = source_page2.find_all('td', class_="right")[6].text


    #debate stats table
    activity_stats = {}

    source_page2 = source_page.find_all('table')     
    for n in source_page2:
      if n.find('tr').text == 'Activity Statistics':
        source_page2 = n
        break


    activity_stats['Forum Posts'] = source_page2.find_all('td', class_="right")[0].text
    activity_stats['Votes Cast'] = source_page2.find_all('td', class_="right")[1].text
    activity_stats['Opinion Arguments'] = source_page2.find_all('td', class_="right")[2].text
    activity_stats['Opinion Questions'] = source_page2.find_all('td', class_="right")[3].text
    activity_stats['Poll Votes'] = source_page2.find_all('td', class_="right")[4].text
    activity_stats['Poll Topics'] = source_page2.find_all('td', class_="right")[5].text


    #the big issues table
    big_issues = {}
    try:
      for td in source_page.find_all("div", id= "issues"):
          Abortion = td.find_all("td", class_="c3")[0].text.split("Comment",1)[0]
      big_issues['Abortion'] = Abortion

      for td in source_page.find_all("div", id= "issues"):
          Affirmative = td.find_all("td", class_="c3")[1].text.split("Comment",1)[0]
      big_issues['Affirmative Action'] = Affirmative

      for td in source_page.find_all("div", id= "issues"):
          Animal = td.find_all("td", class_="c3")[2].text.split("Comment",1)[0]
      big_issues['Animal Rights'] = Animal

      for td in source_page.find_all("div", id= "issues"):
          Barack = td.find_all("td", class_="c3")[3].text.split("Comment",1)[0]
      big_issues['Barack Obama'] = Barack

      for td in source_page.find_all("div", id= "issues"):
          Border = td.find_all("td", class_="c3")[4].text.split("Comment",1)[0]  
      big_issues['Border Fence'] = Border

      for td in source_page.find_all("div", id= "issues"):
          Capitalism = td.find_all("td", class_="c3")[5].text.split("Comment",1)[0]
      big_issues['Capitalism'] = Capitalism

      for td in source_page.find_all("div", id= "issues"):
          Civil = td.find_all("td", class_="c3")[6].text.split("Comment",1)[0]
      big_issues['Civil Unions'] = Civil

      for td in source_page.find_all("div", id= "issues"):
          Death = td.find_all("td", class_="c3")[7].text.split("Comment",1)[0]
      big_issues['Death Penalty'] = Death

      for td in source_page.find_all("div", id= "issues"):
          Drug = td.find_all("td", class_="c3")[8].text.split("Comment",1)[0]
      big_issues['Drug Legalization'] = Drug

      for td in source_page.find_all("div", id= "issues"):
          Electoral = td.find_all("td", class_="c3")[9].text.split("Comment",1)[0]
      big_issues['Electoral College'] = Electoral

      for td in source_page.find_all("div", id= "issues"):
          Environmental = td.find_all("td", class_="c3")[10].text.split("Comment",1)[0]
      big_issues['Environmental Protection'] = Environmental

      for td in source_page.find_all("div", id= "issues"):
          Estate = td.find_all("td", class_="c3")[11].text.split("Comment",1)[0]
      big_issues['Estate Tax'] = Estate

      for td in source_page.find_all("div", id= "issues"):
          European = td.find_all("td", class_="c3")[12].text.split("Comment",1)[0]
      big_issues['European Union'] = European

      for td in source_page.find_all("div", id= "issues"):
          Euthanasia = td.find_all("td", class_="c3")[13].text.split("Comment",1)[0]
      big_issues['Euthanasia'] = Euthanasia

      for td in source_page.find_all("div", id= "issues"):
          Federal = td.find_all("td", class_="c3")[14].text.split("Comment",1)[0]
      big_issues['Federal Reserve'] = Federal

      for td in source_page.find_all("div", id= "issues"):
          Flat = td.find_all("td", class_="c3")[15].text.split("Comment",1)[0]
      big_issues['Flat Tax'] = Flat

      for td in source_page.find_all("div", id= "issues"):
          Free = td.find_all("td", class_="c3")[16].text.split("Comment",1)[0]
      big_issues['Free Trade'] = Free

      for td in source_page.find_all("div", id= "issues"):
          Gay = td.find_all("td", class_="c3")[17].text.split("Comment",1)[0]
      big_issues['Gay Marriage'] = Gay

      for td in source_page.find_all("div", id= "issues"):
          Global = td.find_all("td", class_="c3")[18].text.split("Comment",1)[0]
      big_issues['Global Warming Exists'] = Global

      for td in source_page.find_all("div", id= "issues"):
          Globalization = td.find_all("td", class_="c3")[19].text.split("Comment",1)[0]
      big_issues['Globalization'] = Globalization

      for td in source_page.find_all("div", id= "issues"):
          Gold = td.find_all("td", class_="c3")[20].text.split("Comment",1)[0]
      big_issues['Gold Standard'] = Gold

      for td in source_page.find_all("div", id= "issues"):
          Gun = td.find_all("td", class_="c3")[21].text.split("Comment",1)[0]
      big_issues['Gun Rights'] = Gun

      for td in source_page.find_all("div", id= "issues"):
          Homeschooling = td.find_all("td", class_="c3")[22].text.split("Comment",1)[0]
      big_issues['Homeschooling'] = Homeschooling

      for td in source_page.find_all("div", id= "issues"):
          Internet = td.find_all("td", class_="c3")[23].text.split("Comment",1)[0]
      big_issues['Internet Censorship'] = Internet

      for td in source_page.find_all("div", id= "issues"):
          Iran = td.find_all("td", class_="c3")[24].text.split("Comment",1)[0]
      big_issues['Iran-Iraq War'] = Iran

      for td in source_page.find_all("div", id= "issues"):
          Labor = td.find_all("td", class_="c3")[25].text.split("Comment",1)[0]
      big_issues['Labor Union'] = Labor

      for td in source_page.find_all("div", id= "issues"):
          Legalized = td.find_all("td", class_="c3")[26].text.split("Comment",1)[0]
      big_issues['Legalized Prostitution'] = Legalized

      for td in source_page.find_all("div", id= "issues"):
          Medicaid = td.find_all("td", class_="c3")[27].text.split("Comment",1)[0]
      big_issues['Medicaid & Meidcare'] = Medicaid

      for td in source_page.find_all("div", id= "issues"):
          Medical = td.find_all("td", class_="c3")[28].text.split("Comment",1)[0]
      big_issues['Medical Marijuana'] = Medical

      for td in source_page.find_all("div", id= "issues"):
          Military = td.find_all("td", class_="c3")[29].text.split("Comment",1)[0]
      big_issues['Military Intervention'] = Military

      for td in source_page.find_all("div", id= "issues"):
          Minimum = td.find_all("td", class_="c3")[30].text.split("Comment",1)[0]
      big_issues['Minimum Wage'] = Minimum

      for td in source_page.find_all("div", id= "issues"):
          National = td.find_all("td", class_="c3")[31].text.split("Comment",1)[0]
      big_issues['National Health Care'] = National

      for td in source_page.find_all("div", id= "issues"):
          Retail = td.find_all("td", class_="c3")[32].text.split("Comment",1)[0]
      big_issues['National Retail Sales Tax'] = Retail

      for td in source_page.find_all("div", id= "issues"):
          Occupy = td.find_all("td", class_="c3")[33].text.split("Comment",1)[0]
      big_issues['Occupy Movement'] = Occupy

      for td in source_page.find_all("div", id= "issues"):
          Progressive = td.find_all("td", class_="c3")[34].text.split("Comment",1)[0]
      big_issues['Progressive Tax'] = Progressive

      for td in source_page.find_all("div", id= "issues"):
          Racial = td.find_all("td", class_="c3")[35].text.split("Comment",1)[0]
      big_issues['Racial Profiling'] = Racial

      for td in source_page.find_all("div", id= "issues"):
          Redistribution = td.find_all("td", class_="c3")[36].text.split("Comment",1)[0]
      big_issues['Redistribution'] = Redistribution

      for td in source_page.find_all("div", id= "issues"):
          Smoking = td.find_all("td", class_="c3")[37].text.split("Comment",1)[0]
      big_issues['Smoking Ban'] = Smoking

      for td in source_page.find_all("div", id= "issues"):
          Social_Programs = td.find_all("td", class_="c3")[38].text.split("Comment",1)[0]
      big_issues['Social Programs'] = Social_Programs

      for td in source_page.find_all("div", id= "issues"):
          Social_Security = td.find_all("td", class_="c3")[39].text.split("Comment",1)[0]
      big_issues['Social Security'] = Social_Security

      for td in source_page.find_all("div", id= "issues"):
          Socialism = td.find_all("td", class_="c3")[40].text.split("Comment",1)[0]
      big_issues['Socialism'] = Socialism

      for td in source_page.find_all("div", id= "issues"):
          Stimulus = td.find_all("td", class_="c3")[41].text.split("Comment",1)[0]
      big_issues['Stimulus Spending'] = Stimulus

      for td in source_page.find_all("div", id= "issues"):
          Term = td.find_all("td", class_="c3")[42].text.split("Comment",1)[0]
      big_issues['Term Limits'] = Term

      for td in source_page.find_all("div", id= "issues"):
          Torture = td.find_all("td", class_="c3")[43].text.split("Comment",1)[0]
      big_issues['Torture'] = Torture

      for td in source_page.find_all("div", id= "issues"):
          United = td.find_all("td", class_="c3")[44].text.split("Comment",1)[0]
      big_issues['United Nations'] = United

      for td in source_page.find_all("div", id= "issues"):
          War = td.find_all("td", class_="c3")[45].text.split("Comment",1)[0]
      big_issues['War in Afghanistan'] = War

      for td in source_page.find_all("div", id= "issues"):
          Terror = td.find_all("td", class_="c3")[46].text.split("Comment",1)[0]
      big_issues['War on Terror'] = Terror

      for td in source_page.find_all("div", id= "issues"):
          Welfare = td.find_all("td", class_="c3")[47].text.split("Comment",1)[0]
      big_issues['Welfare'] = Welfare
    except:
      pass      
    
    #collecting all tables
    All_tables = dict({'person_info_table': person_info_table, 'debate_stats': debate_stats,
                       'activity_stats': activity_stats, 'big_issues':big_issues})
    return All_tables

with open('ratings_information.pkl', 'rb') as f:
    debates = pickle.load(f)

id_list = []
for key in debates:
  for name in debates[key][key]['Voter'].keys():
    if name not in id_list:
      id_list.append(name)

id_list.remove("Anonymous")
with open('voters_id.pkl', 'wb') as f:
    pickle.dump(id_list, f)

with open('voters_id.pkl', 'rb') as f:
    id = pickle.load(f)
all_link = ["https://www.debate.org/" + each + "/" for each in id]

# Checking to see if file already exists
if os.path.isfile('user_information.pkl'):
  with open('user_information.pkl', 'rb') as f:
    User_info = pickle.load(f)
else:
  User_info = {}

used_url_list = []
for link in all_link:
  if link not in User_info.keys():
    try:
      User_info[link] = write_user_page_to_file(link)
      used_url_list.append(link)
    except Exception as e:
      print(e)
      time.sleep(60)
      with open('user_information.pkl', 'wb') as f:
        pickle.dump(User_info, f)
  else:
    print("{} is already saved".format(link))

with open('user_information.pkl', 'wb') as f:
    pickle.dump(User_info, f)