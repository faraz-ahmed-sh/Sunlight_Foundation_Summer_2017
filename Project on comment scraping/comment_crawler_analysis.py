'''
ANALYSIS OF COMMENTS
'''
import comment_crawler
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
import numpy as np
from nltk.book import *
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


stop = set(stopwords.words('english'))
stop.update(['-', '&', "'s", '.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '.', 'the', ',', 'and', 'of', ';', 'for', 'that', 'on', 'to', 'a', 'or', 'is', 'in', '’', '"', '”', "" ])


## 1) finding out most common words in quoted texts (policy sections)

def common_words_quoted_texts(type_of_text, city_name, city_dictionary, common_words_limit):
    string_quoted_text = city_dictionary[type_of_text].str.cat(sep=' ').lower()
    words = nltk.tokenize.word_tokenize(string_quoted_text)
    good_words = [i for i in words if i not in stop] # stop words
    fdist = FreqDist(good_words)
    common_quoted_text_20 = fdist.most_common(common_words_limit)
    df = pd.DataFrame(data=common_quoted_text_20, columns=['word', 'count'])
    return df, fdist.plot(common_words_limit, title=city_name)


## 2) finding out most common quoted policy sections (n-grams) and Sentiment Analysis


from nltk.util import ngrams
from collections import Counter

def extract_phrases(string_quoted, length):
	'''
	Finding most common phrases based on the given number of words.
	'''

	phrase_counter = Counter()
	for sentence in string_quoted:
		non_speaker = re.compile('[A-Za-z]+: (.*)')
		for sent in nltk.sent_tokenize(sentence):
			strip_speaker = non_speaker.match(sent)
			if strip_speaker is not None:
				sent = strip_speaker.group(1)

			words = nltk.word_tokenize(sent)
			for phrase in ngrams(words, length):
				phrase_counter[phrase] += 1

				#extract_phrases(sentence, phrase_counter, 3)

	most_common_phrases = phrase_counter.most_common(10)
	most_common_phrases_new = []

	for k,v in most_common_phrases:

		p = ' '.join(k)
		most_common_phrases_new.append((p, v))


	return most_common_phrases_new


def top_policy_sections_commented(type_of_data, option, length):

    total_sentence_count_list = []

    if type(type_of_data) == list: #if its a list of dictionaries of all the cities

        for name, dictionary in type_of_data:

            if option == "most_common_policy": # if the option is to find out comments of popular sections of each city
                list_of_lists_sentences = list_of_lists_of_sentences(name, dictionary, length)[0]
                
                if len(list_of_lists_sentences) != 0: # don't print results for cities with no comments. (???)
                    sentiment_analysis_list = sentiment_analysis(list_of_lists_sentences, name, dictionary)
                    sentimental_analysis_graphs = sentimental_analysis_charts(sentiment_analysis_list, "both")   
                    print (sentimental_analysis_graphs)
                    
            else:
                string_quoted_text_list = dictionary['comment_text'].dropna().tolist()
                sentiment_analysis_list = sentiment_analysis(string_quoted_text_list, name, dictionary)
                #print("--------minus 3 and minus 4 --------", sentiment_analysis_list[-3], sentiment_analysis_list[-4])
                total_sentence_count_list.append(sentiment_analysis_list[-3])
                total_sentence_count_list.append(sentiment_analysis_list[-4])
                
                sentimental_analysis_graphs = sentimental_analysis_charts(sentiment_analysis_list, "both")   
                print (sentimental_analysis_graphs)

            if len(total_sentence_count_list) != 0:
                if total_sentence_count_list[-1] == "San Francisco":
                    sentimental_analysis_graphs_tot_sent = sentimental_analysis_charts(total_sentence_count_list, "tot_sent")
                    print (sentimental_analysis_graphs_tot_sent)
                
    else: # it its one big dictionary containing data for all the cities

        name = "All Cities"

        if option == "most_common_policy": # if the option is to find out comments of popular sections
            list_of_lists_sentences, most_common_phrases  = list_of_lists_of_sentences(name, type_of_data, length)
            sentiment_analysis_list = sentiment_analysis(list_of_lists_sentences, name, type_of_data)
            sentimental_analysis_graphs = sentimental_analysis_charts(sentiment_analysis_list, "both")
            return (sentimental_analysis_graphs, sentiment_analysis_list[-2], sentiment_analysis_list[-1], most_common_phrases)

        else: # if the option is to find out all the comments of all policy sections
            string_quoted_text_list = type_of_data['comment_text'].dropna().tolist()
            sentiment_analysis_list = sentiment_analysis(string_quoted_text_list, name, type_of_data)
            sentimental_analysis_graphs = sentimental_analysis_charts(sentiment_analysis_list, "both")
            return [sentiment_analysis_list, sentiment_analysis_list[-2], sentiment_analysis_list[-1]]


def most_common_phrases_to_list(city_name, city_dictionary, most_common_phrases):
    '''
    Convert a list of most common phrases into a list of lists of actual sentences.
    '''
    
    list_of_lists_sentences = []
    for string_phrase, len_string_phrase in most_common_phrases:
        actual_comment_filter = city_dictionary[city_dictionary['quoted_text'].astype(str).str.contains(string_phrase)]
        comment_list_sentiment = actual_comment_filter['comment_text'].tolist()
        #print("COMMENT LIST", comment_list_sentiment)
        for comment in comment_list_sentiment:
            if comment not in list_of_lists_sentences:
                list_of_lists_sentences.append(comment)
        #list_of_lists_sentences.append(comment_list_sentiment)

    return (list_of_lists_sentences, city_name)


def list_of_lists_of_sentences(name, dictionary, length):

    string_quoted_text_list = dictionary['quoted_text'].dropna().tolist()
    most_common_phrases = extract_phrases(string_quoted_text_list, length)
    #for k,v in most_common_phrases:
    #    print(k,v)   
    list_of_lists_sentences, city_name = most_common_phrases_to_list(name, dictionary, most_common_phrases)
    return list_of_lists_sentences, most_common_phrases



def sentiment_scores(sentence_list, city_dictionary, total_sentence_count, neg_count, neg_polarity, neu_count, neu_polarity, pos_count, pos_polarity):
    
    sid = SentimentIntensityAnalyzer()
    negative_comments = []
    positive_comments = []
    neutral_comments = []
    
    for sentence in sentence_list:
        
        ss = sid.polarity_scores(sentence)
        if ss['neg'] >= 0.3 and ss['neu'] <0.7 and ss['pos'] <0.3:
            neg_count += 1
            neg_polarity += ss['neg']
            negative_comments.append(sentence)
            print("negative sentence:", sentence)

        elif ss['neu'] >= 0.7 and ss['neg'] <0.3 and ss['pos'] <0.3:
            neu_count += 1
            neu_polarity += ss['neu']
            neutral_comments.append(sentence)
            #print("neutral sentence:", sentence)

        elif ss['pos'] >= 0.3 and ss['neu'] <0.7 and ss['neg'] <0.3:
            pos_count += 1
            pos_polarity += ss['pos']
            positive_comments.append(sentence)
            print("positive sentence:", sentence)

        total_sentence_count += 1
    return total_sentence_count, neg_count, neg_polarity, neu_count, neu_polarity, pos_count, pos_polarity, negative_comments, positive_comments


def sentiment_analysis(list_of_lists_of_sentences, city_name, dictionary):
    neg_count = 0
    neu_count = 0
    pos_count = 0
    neg_polarity = 0
    neu_polarity = 0
    pos_polarity = 0
    
    total_sentence_count = 0
    
    total_sentence_count, neg_count, neg_polarity, neu_count, neu_polarity, pos_count, pos_polarity, neg_sentences, pos_sentences = sentiment_scores(list_of_lists_of_sentences, dictionary, total_sentence_count, neg_count, neg_polarity, neu_count, neu_polarity, pos_count, pos_polarity)
        
    print()
    print("total_comments:", total_sentence_count, "---", "city name:", city_name)
    
    if total_sentence_count == 0:
        total_sentence_count = 1
    
    avg_neg_polarity = neg_polarity/total_sentence_count
    avg_neu_polarity = neu_polarity/total_sentence_count
    avg_pos_polarity = pos_polarity/total_sentence_count
                
    return ["neg count", neg_count, "neu_count", neu_count, "pos_count", pos_count, "avg_neg_polarity", avg_neg_polarity, "avg_neu_polarity", avg_neu_polarity, "avg_pos_polarity", avg_pos_polarity, city_name, total_sentence_count, neg_sentences, pos_sentences]

'''
4) Likes/Replies Analysis
'''

def likes_replies_analysis(count, option, all_cities_dataframe):
    high_likes = all_cities_dataframe[all_cities_dataframe[option] >= count]
    high_likes = high_likes.reset_index()
    high_likes_comments = high_likes['comment_text']
    for high_like_comment in high_likes_comments:
        print()
        print('\033[1m' + "comment:")
        print()
        print('\033[0m' + high_like_comment)
    
    return high_likes


def transform_likes_replies(likes_x, likes_y, replies_x, replies_y, dictionaries):

    all_likes = []
    all_replies = []

    for name, city in dictionaries:
        if name not in likes_x:
            likes_x.append(name)
            likes_y.append(0)
            if name not in replies_x:
                replies_x.append(name)
                replies_y.append(0)
        if name not in replies_x:
            replies_x.append(name)
            replies_y.append(0)

    return likes_x, likes_y, replies_x, replies_y
