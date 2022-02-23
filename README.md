# Debate_Webscraper
Arguments, Votes, User Information Scraper for Debate.org
Shilong Wang, Sungbin Youk, & René Weber*
Media Neuroscience Lab - UC Santa Barbara
*A special acknowledgment and thank you to research assistant Shilong who foremost developed this notebook as part of a summer project in 2021 with the supervision of Sungbin Youk and René Weber.


Welcome to the Python Google Colab Notebook for scraping arguments, votes, and user information from Debate.org! This notebook was created by Shilong Wang along with the supervision and guidance from the Media Neuroscience Lab at UCSB to introduce webscraping to social science researchers .

This notebook collects various information from debates that are in post-voting status. Specifically, there are three types of information that are scraped. First, information about debates includes the title of the debate, the user name of the winner, the start date of the debate, number of comments and more. Second, the arugment information includes the number of rounds and the arguments made in each round. Third, information about the user is also collected. The output is stored in either csv or pickle files.

Specifically, this notebook has three main sections: first, setting up the output directory on Google Drive; second, preparing the environment; third, running the code (there are 5 parts of the code, each with a different purpose). For each section, there is detailed instruction. Please follow the guidelines in these three sections in order as each step builds on the previous one.

Disclaimer: This code may automatically ignore a few debates when encountering errors of any sort. However, please rest assured that the amount of such circumstances will be very small and will not influence the overall accuracy of the data.
