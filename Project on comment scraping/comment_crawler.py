# Assignment: Open Data Policies comments scrape

import bs4
import queue
import json
import sys
import csv
import urllib
import collections
import pandas as pd
import distance
import jellyfish
import sys
#nltk.download()

#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from nltk import tokenize
#from textblob import TextBlob
#from textblob import TextBlob
#textblob.download()




starting_urls_list = ["https://mymadison.io/documents/city-of-buffalo-open-data-policy", 
                      "https://mymadison.io/documents/durham-open-data-policy",
                      "https://mymadison.io/documents/city-of-tyler-data-policy",
                      "https://mymadison.io/documents/city-of-glendale-draft-open-data-resolution",
                      "https://mymadison.io/documents/metro-nashville-government-open-data-policy",
                      "https://mymadison.io/documents/city-of-syracuse-open-data-policy",
                      "https://mymadison.io/documents/napervilleopendatapolicy",
                      "https://mymadison.io/documents/bart-open-data-policy",
                      "https://mymadison.io/documents/san-francisco-open-data-legislation-2014"]

starting_url = "https://mymadison.io/documents/city-of-buffalo-open-data-policy?comment_page=1"


'''
AUXILLARY FUNCTIONS
'''

def simple_crawl(starting_url):
    '''
    Scrapes the full webpage from a starting url.

    Inputs:
        starting_url: string
    Returns:
        a soup object
    '''    
    page = urllib.request.urlopen(starting_url)
    if page is not None:
        soup = bs4.BeautifulSoup(page, "html")
        return soup

def comment_id(comment):
    comment_id = comment.get('id')
    return comment_id


def name(comment):
    name_date = comment.find("div", class_="media-body media-middle")
    name = name_date.find("span")
    name_final = name.string.strip()
    return name_final, name_date

def datetime(comment):
    name_date = name(comment)[1]
    time = name_date.find("time")
    datetime_final = time.get("datetime")[:-6]
    datetime_final_1 = datetime_final.replace("T", " ")
    return datetime_final_1

def likes_count(comment):
    name_date = name(comment)[1]
    likes = name_date.find("span", class_="action-count")
    return likes.string.strip()

def quoted_comment(comment):
    comments = comment.find("div", class_="comment-content")
    quoted_comment = comments.find("blockquote")
    if quoted_comment is not None:
        quoted_comment_final = quoted_comment.text.strip()
        return quoted_comment_final, comments
    else:
        return None, comments


def actual_comment(comment):
    comments = comment.find("div", class_="comment-content")
    actual_comments = comments.find_all("p", recursive=False)
    
    complete_str_aux = ''
    complete_str_str = ''
    
    for child in actual_comments:
        complete_str_aux += str(child)
        complete_str_str += str(child.text)
    return complete_str_aux, complete_str_str


def reply_ids(comment):
    
    replies = comment.find_all("div", class_="comment")
    if replies is not None:
        reply_id_list = []
        for reply in replies:
            reply_id=reply.get('id')
            reply_id_list.append(reply_id)

        return reply_id_list
    else:
        return []


def find_total_num_pages(starting_url):
    soup = simple_crawl(starting_url)
    next_page = soup.find_all("ul", class_="pagination")
    
    for page in next_page:
        pages = page.find_all("a")
        total_num_pages = pages[-2].get("href")
        return int(total_num_pages[-1])


def calling_functions(commentators, comments_dictionary, comment_number):
    
    for comment in commentators:
        
        comment_id_f = comment_id(comment)
        name_f =  name(comment)
        timedate_f = datetime(comment)
        likes_count_f = likes_count(comment)
        quoted_comment_f = quoted_comment(comment)
        actual_comment_f, actual_comment_str =  actual_comment(comment)
        reply_ids_f = reply_ids(comment)


        comments_dictionary[comment_number] = [comment_id_f,name_f[0], timedate_f, 
                                      likes_count_f, quoted_comment_f[0],
                                       actual_comment_str, actual_comment_f, reply_ids_f]
        comment_number += 1
    
    return comments_dictionary, comment_number


'''
Function to scrape a particular open data policy and put it into a dataframe.
'''

def scrape_all_pages(starting_url):
    '''
    This functions scrapes the required data from all the webpages for a PARTICULAR starting url of a Madison webpage.
    '''
    comments_dictionary = {}
    num_pages_to_crawl = find_total_num_pages(starting_url)
    
    if num_pages_to_crawl is None:
        num_pages_to_crawl = 1
        
    loop_number = 0
    comment_number = 1

    while loop_number < num_pages_to_crawl:
    
        soup = simple_crawl(starting_url)
        commentators = soup.findAll("li", class_="comment floating-card")
        
        comments_dictionary, comment_number = calling_functions(commentators, comments_dictionary, comment_number)
        
        next_page = soup.find_all("ul", class_="pagination")
        for page in next_page:
            pages = page.find_all("a")
            starting_url = pages[-1].get("href")
        
        loop_number += 1
        
    return comments_dictionary


def convert_dict_pandas(comments_dictionary):
    
    df = pd.DataFrame(comments_dictionary)
    df = df.transpose()
    df.columns = ['comment_id', 'author', 'datetime', 'num_likes', 'quoted_text', 'comment_text', 'comment_text_aux', 'reply_ids']
    
    # converting str datetime into datetime pandas format
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df


'''
Function to scrape all the open data policies and put them into dataframes.
'''

all_cities_names = ['Buffalo', 'Durham', 'Tyler', 'Glendale', 'Nashville', 'Syracuse', 'Naperville', 'Bart', 'San Francisco']

def go_all_madison_websites(starting_urls_list):
    '''
    This function scrapes the comments from all the Madison related webistes for cities that have
    launched open data policies and converts them into pandas dataframe objects.
    
    Returns:
        DataFrame object for each city's open data policy.
    '''
    i = 0
    all_madison_websites_dfs = []
    all_cities_dataframe = pd.DataFrame()
    for starting_url in starting_urls_list:
        #print(starting_url)
        comments_dictionary = scrape_all_pages(starting_url)
        get_dict_to_pandas = convert_dict_pandas(comments_dictionary)
        #relative_url = starting_url.split('/')[-1]
        get_dict_to_pandas['city_name'] = all_cities_names[i]
        all_madison_websites_dfs.append((all_cities_names[i], get_dict_to_pandas))
        all_cities_dataframe = all_cities_dataframe.append(get_dict_to_pandas)
        i += 1
        
    return all_madison_websites_dfs, all_cities_dataframe





