# CS122: Course Search Engine Part 1

import re
import util
import bs4
import queue
import json
import sys
import csv
import urllib

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of',
                    'on',  'or',  's',  'sequence',  'so',  'social',  'students',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'topics',  'units', 'we', 'were', 'which', 'will', 'with', 'yet'])

#starting_url = "http://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/index.html"
starting_url = "https://mymadison.io/documents/city-of-buffalo-open-data-policy?comment_page=1"
limiting_domain = "classes.cs.uchicago.edu"
#starting_url = "http://mymadison.io/"



def simple_crawl(starting_url):
    '''
    Scrapes the valid urls from a starting url.

    Inputs:
        starting_url: string
    Returns:
        List of url's that have been crawled through
    '''    
    page = urllib.request.urlopen(starting_url)
    if page is not None:
        soup = bs4.BeautifulSoup(page, "lxml")
        #print(soup)

        commentators = soup.find_all("div", class_="media-body media-middle")
        print(commentators)



    '''

    html = util.get_request(starting_url)
    #check1 = set()
    #filtered_url_list = []

    if html is not None:
        text = util.read_request(html)
        print(text)
        soup = bs4.BeautifulSoup(text, "lxml")
    '''
    '''
        tag_list = soup.find_all("a")

        # get a list of clean urls
        for link1 in tag_list:
            initial_url = link1.get('href')
            if initial_url is not None:
                if util.is_absolute_url(initial_url) == False:
                    if "#" in initial_url:
                        initial_url = util.remove_fragment(initial_url)
                    initial_url = util.convert_if_relative_url(starting_url, initial_url)

                if initial_url is not None:   
                     if (util.is_url_ok_to_follow(initial_url, limiting_domain)) and (initial_url not in check1):
                        check1.add(initial_url)
                        filtered_url_list.append(initial_url)

        return filtered_url_list
        '''
        #print(soup)


def get_indexer(starting_url, num_pages_to_visit, course_map):
    '''
    Obtains course names from a specified url

    Inputs:
        url: string
    Returns:
        indexer: dictionary
    '''

    links_list = get_links(starting_url)

    q = queue.Queue()
    check_set = set()
    check_set.add(links_list[0])
    for urls in links_list:
        check_set.add(urls)
    visited_list_url = []

    for link2 in links_list:
        q.put(link2)

    indexer = {}

    # using while loop to crawl into pages
    while (len(visited_list_url) < num_pages_to_visit) and q.qsize() != 0:
        first_out = q.get()
        if first_out is not None:
            first_out_request = util.get_request(first_out)
            if first_out_request is not None:
                first_out_https = util.get_request_url(first_out_request)
                if util.is_url_ok_to_follow(first_out_https, limiting_domain):
                    if first_out_https is not None and first_out_https not in visited_list_url:
                        visited_list_url.append(first_out_https)
                        get_course_names(first_out_request, indexer, course_map)
                        new_links = get_links(first_out_https)
                        for link3 in new_links:
                            if link3 not in check_set:
                                q.put(link3)
                                check_set.add(link3)

    return indexer


def index_adding(indexer, complete_words_list, course_code, course_map):
    '''
    Auxiliary function that adds words to the index

    Inputs:
        indexer: dictionary
        complete_words_list: list_rows
        course_code: integer
        course_map: JSON
    '''

    for word in complete_words_list:
        if word not in indexer and word not in INDEX_IGNORE and course_code in course_map:
            indexer[word] = []
            indexer[word].append(course_map[course_code])
        else:
            if word not in INDEX_IGNORE and course_code in course_map and course_map[course_code] not in indexer[word]:
                indexer[word].append(course_map[course_code])


def regular_expression(tag):
    '''
    Auxiliary function that filters words.

    Inputs:
        tag: list
    Returns:
        Tuple
    '''

    words = tag[0].text.split()
    course_code = words[0] + " " + words[1].replace(".","")
    
    words_indexer_title = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', tag[1].text.lower())
    words_indexer_desc = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', tag[2].text.lower())
    
    complete_words_list = words_indexer_title + words_indexer_desc

    return (complete_words_list, course_code)


def get_course_names(https, indexer, course_map):
    '''
    Obtains course names from a specified url

    Inputs:
        https: string
        indexer: dictionary
        course_map: JSON 
    Returns:
        indexer: dictionary
    '''

    text = util.read_request(https)
    soup = bs4.BeautifulSoup(text, "lxml")
    tag_list = soup.find_all("div", class_= "courseblock main")
    
    if tag_list != {}:
        for tag in tag_list:

            # check if the tag is a sequence
            if util.find_sequence(tag):
                tag_seq_child = tag.findChildren()
                words_and_coursecode = regular_expression(tag_seq_child)
                tag_bro = tag.nextSibling

                # check if the tag is subsequence and index in all the subsequences
                while util.is_subsequence(tag_bro):
                    tag_seq_seq_child = tag_bro.findChildren()
                    words_and_coursecode_seq = regular_expression(tag_seq_seq_child)
                    complete_words_list_2 = words_and_coursecode[0] + words_and_coursecode_seq[0]
                    index_adding(indexer, complete_words_list_2, words_and_coursecode_seq[1], course_map)
                    tag_bro = tag_bro.nextSibling
            else:
                tag_child = tag.findChildren()
                words_and_coursecode_non_seq = regular_expression(tag_child)
                index_adding(indexer, words_and_coursecode_non_seq[0], words_and_coursecode_non_seq[1], course_map)


'''
def go(num_pages_to_crawl, course_map_filename, index_filename):
    
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs: 
        CSV file of the index index.
    

    with open(course_map_filename) as json_data:
            course_map = json.load(json_data)

    list_rows = []

    get_indexer_1 = get_indexer(starting_url, num_pages_to_crawl, course_map)

    out = csv.writer(open(index_filename,"w"))

    # presenting the right output into the CSV file
    for key, value in get_indexer_1.items():
        for course_identifier in value:
            identifier_string = '|'.join([str(course_identifier), key])
            list_rows.append(identifier_string)

    for row in list_rows:
        out.writerow([row])



if __name__ == "__main__":
     usage = "python3 crawl.py <number of pages to crawl>"
     args_len = len(sys.argv)
     course_map_filename = "course_map.json"
     index_filename = "catalog_index.csv"
     if args_len == 1:
         num_pages_to_crawl = 1000
     elif args_len == 2:
         try:
             num_pages_to_crawl = int(sys.argv[1])
         except ValueError:
             print(usage)
             sys.exit(0)
     else:
         print(usage)    
         sys.exit(0)

go(num_pages_to_crawl, course_map_filename, index_filename)
'''