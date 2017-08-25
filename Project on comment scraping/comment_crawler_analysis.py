import comment_crawler
from graphs_and_charts import *
from authors_names import *
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
import numpy as np
from nltk.book import *
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.util import ngrams
from collections import Counter

stop = set(stopwords.words('english'))
stop.update(['-', '&', "'s", '.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '.', 'the', ',', 'and', 'of', ';', 'for', 'that', 'on', 'to', 'a', 'or', 'is', 'in', '’', '"', '”', "", 'would', 'could', "``", "''", 'also', 'make'])

'''
FUNCTIONS TO ANALYZE OPEN DATA POLICIES
'''


def common_words_quoted_texts(type_of_text, city_name, city_dictionary, common_words_limit, option):
    '''
    Calculates the most popular words based on their frequency in comment-text and quoted-text.

    Returns:
        a graph of popular words
        a dataframe that includes a count of most popular words, given a limit of words to display.
    '''
    string_quoted_text = city_dictionary[type_of_text].str.cat(sep=' ').lower()
    words = nltk.tokenize.word_tokenize(string_quoted_text)
    good_words = [i for i in words if i not in stop] # stop words
    fdist = FreqDist(good_words)
    common_text_20 = fdist.most_common(common_words_limit)
    df = pd.DataFrame(data=common_text_20, columns=['Word', type_of_text + '_freq'])
    if option == "both":
        plot = fdist.plot(common_words_limit, title=city_name)
        return df
    else:
        return df


def ratio_quoted_freq_with_policy_freq(line_graph_option, type_of_text, city_name, city_dictionary, common_words_limit, policy_text, option, sort_option):
    '''
    This function compares the quoted-text/comment-text frequency with the policy-text frequency.

    Returns:
        a graph for the ratio of quoted-text/comment-text frequency to policy-text frequency (for words).
        a dataframe that includes a ratio of quoted-text/comment-text frequency to policy-text frequency (for words).
    '''
    count = 1
    dict_quoted_freq_with_policy_freq = {}

    policy_text_tokenize = nltk.tokenize.word_tokenize(policy_text)
    df_word_count = common_words_quoted_texts(type_of_text, city_name, city_dictionary, common_words_limit, option)
    df_quoted_popular_words = df_word_count['Word'].tolist()

    # check to see if and count how many quoted/commented word comes up in the policy text
    if df_quoted_popular_words != []:

        for word1 in df_quoted_popular_words:
            for word2 in policy_text_tokenize:
                if word1 == word2:
                    if word1 in dict_quoted_freq_with_policy_freq:
                        dict_quoted_freq_with_policy_freq[word1] += 1
                    else:
                        dict_quoted_freq_with_policy_freq[word1] = count

        # joining two dataframes (one with count of quoted/commented words and another with count of policy text words) on a key
        dict_to_pd = pd.DataFrame.from_dict(dict_quoted_freq_with_policy_freq, orient="index").reset_index()
        dict_to_pd.columns = ['Word', 'Freq. in policy text']
        dict_to_pd_2 = pd.merge(dict_to_pd, df_word_count, how='left', on=['Word'])
        type_of_text_update = type_of_text + '_freq'
        dict_to_pd_2['Ratio'] = dict_to_pd_2[type_of_text_update]/dict_to_pd_2['Freq. in policy text']
        dict_to_pd_2 = dict_to_pd_2[['Word', type_of_text_update, 'Freq. in policy text']]
        
        if sort_option == "descending":
            dict_to_pd_2 = dict_to_pd_2.round(2).sort_values('Ratio', ascending=False).reset_index().drop('index', axis=1)
        elif sort_option == "ascending":
            dict_to_pd_2 = dict_to_pd_2.round(2).sort_values('Ratio', ascending=True).reset_index().drop('index', axis=1)

        # option to produce either a graph with two variables (word frequency of both variables - policy text and quoted/commented text or a ratio of both) 
        #or one variable (a ratio of policy text vs. quoted/comment text)
        my_xticks = dict_to_pd_2['Word'].tolist()

        if line_graph_option == "double_line_graph":

            y1 = dict_to_pd_2['Freq. in policy text'].tolist()
            y2 = dict_to_pd_2[type_of_text_update].tolist()
            
            if type_of_text == "comment_text" and line_graph_option == "double_line_graph":
                labels = ('Freq. in policy text', 'comment text freq')
            elif type_of_text == "quoted_text" and line_graph_option == "double_line_graph":
                labels = ('Freq. in policy text', 'quoted text freq')
            line_graph(my_xticks, y1, y2, labels, city_name, type_of_text, line_graph_option)

        elif line_graph_option == "single_line_graph":

            y1 = dict_to_pd_2['Ratio'].tolist()
            labels = ('ratio',)
            line_graph(my_xticks, y1, None, labels, city_name, type_of_text, line_graph_option)

        return dict_to_pd_2


def extract_phrases(string_quoted, length):
	'''
	Finding most common phrases, given a fixed number of words that are quoted by different people.
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

	most_common_phrases = phrase_counter.most_common(10)
	most_common_phrases_new = []

	for k,v in most_common_phrases:

		p = ' '.join(k)
		most_common_phrases_new.append((p, v))

	return most_common_phrases_new


def sentiment_analysis_output(type_of_data, option, length):
    '''
    Main function for sentiment analysis.

    Produces sentimental analysis graphs given a dataframe (containing data for all cities).
    '''

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
    Find out actual comments given a popular quoted policy text.
    '''
    list_of_lists_sentences = []
    for string_phrase, len_string_phrase in most_common_phrases:
        actual_comment_filter = city_dictionary[city_dictionary['quoted_text'].astype(str).str.contains(string_phrase)]
        comment_list_sentiment = actual_comment_filter['comment_text'].tolist()

        for comment in comment_list_sentiment:
            if comment not in list_of_lists_sentences:
                list_of_lists_sentences.append(comment)

    return (list_of_lists_sentences, city_name)


def list_of_lists_of_sentences(name, dictionary, length):
    '''
    Find out actual comments of all the popular quoted policy texts.
    '''
    string_quoted_text_list = dictionary['quoted_text'].dropna().tolist()
    most_common_phrases = extract_phrases(string_quoted_text_list, length)
    #for k,v in most_common_phrases:
    #    print(k,v)   
    list_of_lists_sentences, city_name = most_common_phrases_to_list(name, dictionary, most_common_phrases)
    return list_of_lists_sentences, most_common_phrases


def sentiment_scores(sentence_list, city_dictionary, total_sentence_count, neg_count, neu_count, pos_count):
    '''
    Use the sentiment analyzer "Vader" to calculate the compound, negative, neutral and positive polarity scores for each comment.
    '''
    sid = SentimentIntensityAnalyzer()
    negative_comments = []
    positive_comments = []
    neutral_comments = []
    
    for sentence in sentence_list:

        ss = sid.polarity_scores(sentence)

        # Typical threshold values as mentioned in:
        # https://github.com/cjhutto/vaderSentiment
        # They were, however, modified slightly based on trial-and-error

        if ss['compound'] <= -0.2:
            neg_count += 1
            negative_comments.append(sentence)

        elif ss['compound'] > -0.2 and ss['compound'] < 0.7:
            neu_count += 1
            neutral_comments.append(sentence)

        elif ss['compound'] >= 0.7:
            pos_count += 1
            positive_comments.append(sentence)

        total_sentence_count += 1
    return total_sentence_count, neg_count, neu_count, pos_count, negative_comments, positive_comments


def sentiment_analysis(list_of_lists_of_sentences, city_name, dictionary):
    '''
    Computes the sentence count.
    '''
    neg_count = 0
    neu_count = 0
    pos_count = 0
    
    total_sentence_count = 0
    
    total_sentence_count, neg_count, neu_count, pos_count, neg_sentences, pos_sentences = sentiment_scores(list_of_lists_of_sentences, dictionary, total_sentence_count, neg_count, neu_count, pos_count)
        
    print("total_comments:", total_sentence_count, " | ", city_name)
    
    if total_sentence_count == 0:
        total_sentence_count = 1
                
    return ["negative count", neg_count, "neutral count", neu_count, "positive count", pos_count, city_name, total_sentence_count, neg_sentences, pos_sentences]


def likes_replies_analysis(count, option, all_cities_dataframe):
    '''
    Filter replies count or likes count of each comment, given a number of count for which the analysis should be done.
    '''
    if type(option) == list:
        high_likes = all_cities_dataframe[(all_cities_dataframe[option[0]].apply(int) >= count) & (all_cities_dataframe[option[1]].apply(int) >= count)]
    else:
        high_likes = all_cities_dataframe[all_cities_dataframe[option] >= count]

    high_likes = high_likes.reset_index()
    high_likes_comments = high_likes['comment_text']

    for high_like_comment in high_likes_comments:
        print()
        print('\033[1m' + "comment:")
        print()
        print('\033[0m' + high_like_comment)
    
    return high_likes


def authors_details(dictionary):
    '''
    Appends characteristics of authors' such as their positions, company name and category work in the dataframe.
    '''  
    positions = []
    company_names = []
    category = []
    authors = []

    for name in dictionary['author']:
        for name_2 in authors_names:
            if name == name_2[0]:
                authors.append(name_2[0])
                positions.append(name_2[1])
                company_names.append(name_2[2])
                category.append(name_2[3])
    return authors, positions, company_names, category


def authors_details_dataframe(dictionary):
    '''
    Appends characteristics of authors' such as their positions, company name and category work in the dataframe.
    '''
    authors, positions, company_names, category = authors_details(dictionary)
    dictionary['Position'] = positions
    dictionary['Company_name'] = company_names
    dictionary['Category_work'] = category
    dictionary = dictionary[['comment_id', 'author', 'Position', 'Company_name', 'Category_work', 'datetime', 'num_likes', 'quoted_text', 'comment_text', 'comment_text_aux', 'reply_ids', 'city_name']]
    return dictionary


def authors_details_analysis(column, df):
    '''
    Groupby's authors' details based on a certain characteristic.
    '''
    output = df.groupby([column]).size().reset_index().rename(columns={0:'count'})
    #print(output)
    output = output.sort_values("count", ascending=False).reset_index()
    return output


def support_n_rejection_analysis(all_madison_dfs):
    '''
    Finds the count of support and rejection for each policy.
    ''' 
    support_x = []
    rejection_x = []
    city_names = []

    for name, city, policy, support in all_madison_dfs:
        support_x.append(support[0])
        rejection_x.append(support[1])
        city_names.append(name)

    return support_x, rejection_x, city_names


