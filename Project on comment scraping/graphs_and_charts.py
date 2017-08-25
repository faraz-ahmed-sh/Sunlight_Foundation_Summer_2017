from comment_crawler import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from matplotlib.ticker import MultipleLocator
import numpy as np


'''
FUNCTIONS TO MAKE GRAPHS AND CHARTS
'''

def sentimental_analysis_charts(list_, option):
    '''
    Display figures of sentiment analysis and total count of comments for each city.
    '''
    
    if option == "both":
    
        fig = plt.figure()
        x_objects = [i for i in list_[:6] if type(i) == str]
        y_pos = np.arange(len(x_objects))
        y_objects = [i for i in list_[:6] if type(i) == int]

        plt.bar(y_pos, y_objects, align='center', alpha=0.7, color="red")
        plt.xticks(y_pos, x_objects)
        plt.ylabel('Count of comments')
        plt.title('Sentiment Analysis -' + " " + list_[-4], weight="bold")
        plt.tight_layout()
        plt.show()
        fig.savefig('images/' + 'sentiment-count-' + list_[-4] + '.png', dpi = 200)
    
    elif option == "tot_sent":
    
        # Chart 2 for the count of total sentences

        x_objects = all_cities_names

        #x_objects = ['Buffalo', 'Durham', 'Tyler', 'Glendale', 'Nashville', 'Syracuse', 'Naperville', 'Bart', 'San Francisco']

        #x_objects = [i for i in list_ if type(i) == str]
        y_pos = np.arange(len(x_objects))
        y_objects = [i for i in list_ if type(i) == int]
        
        fig = plt.figure()
        plt.bar(y_pos, y_objects, align='center', alpha=0.7, color="green")
        plt.xticks(y_pos, x_objects, rotation=70)
        plt.ylabel('Count of comments')
        plt.title('City-wise all comments count', weight="bold")
        plt.tight_layout()
        plt.show()
        fig.savefig('images/' + 'total-comments.png', dpi = 200)


def horizontal_bar(x_objects, y_objects, xlabel, title):
    '''
    Display a horizontal bar.
    '''
    
    fig = plt.figure()
    y_pos = np.arange(len(x_objects))
    plt.barh(y_pos, y_objects, align='center', alpha=0.7, color="red")
    plt.xticks(y_objects)
    plt.yticks(y_pos, x_objects)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + title + '.png', dpi = 200)


def line_graph(my_xticks, y1, y2, labels, city_name, type_text, line_graph_option):
    '''
    Display a graph that includes a ratio of policy text words to quoted text words.
    '''

    fig, ax = plt.subplots(figsize=(7, 4))
    x = range(len(my_xticks))
    plt.title(city_name)
    plt.xticks(x, my_xticks, rotation=90)
    plt.plot(x, y1, 'r')
    
    if line_graph_option == "double_line_graph":
        plt.plot(x, y2, 'b')
    
    #plt.legend(labels, loc='best')
    #ax.legend_.remove()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + city_name + '-ratio-' + type_text + '-to-policy-text' + '.png', dpi = 200)


def pie_chart(sizes, labels, savefigcaption):
    '''
    Display a pie chart to show proportion of positive, negative and neutral comments.
    '''
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, autopct='%1.1f%%',
            shadow=True, startangle=90, pctdistance=1.125)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(labels, loc="upper corner")
    plt.tight_layout()
    plt.show()
    fig1.savefig('images/' + savefigcaption + '.png', dpi = 200)


def transform_likes_replies(likes_x, likes_y, replies_x, replies_y, dictionaries):

    all_likes = []
    all_replies = []

    for name, city, policy_text, support in dictionaries:
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


def likes_replies_chart(ylabel, legend_, title, likes_x, likes_y, replies_x, replies_y, dictionaries, option):
    '''
    Display the chart for likes/replies count for each city.
    '''
    if option == "likes_replies_analysis":

        likes_x, likes_y, replies_x, replies_y = transform_likes_replies(likes_x, likes_y, replies_x, replies_y, dictionaries)

    N = len(likes_x) # total numbmer of cities
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, likes_y, width, color='r')
    rects2 = ax.bar(ind + width, replies_y, width, color='y')
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(likes_x, rotation=65)
    ax.yaxis.set_major_locator(MultipleLocator(2.0))
    ax.legend((rects1[0], rects2[0]), legend_)

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.99*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + title + '.png', dpi = 200)


def horizontal_bar_from_dataframe(df, yaxis, xaxis, xlabel):
    '''
    Make horizontal bar given a dataframe.
    '''
    all_categories = df[yaxis]
    ax = df[[yaxis, xaxis]].plot(kind="barh")
    fig = ax.get_figure()
    ax.set_xlabel(xlabel)
    #ax.set_title('Who comments the most?')
    ax.set_yticklabels(all_categories)
    fig.tight_layout()
    ax.legend_.remove()
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + 'who-comments-the-most' + yaxis + '.png', dpi=200)


def horizontal_stacked_bar_from_dataframe(df, y1, y2, xaxis, xlabel, title):
    '''
    Make stacked horizontal bar given a dataframe.
    '''
    ax = df.pivot(y1, y2, xaxis).plot.barh(stacked=True, colormap='Set1')
    
    fig = ax.get_figure()
    ax.set_xlabel(xlabel)
    ax.set_ylabel('')
    #ax.set_title(title)
    lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + title + '.png', dpi=200, bbox_extra_artists=(lgd,), bbox_inches='tight')


def vertical_bar_from_dataframe(cities_all_comments_count, ylabel):
    x_axis = cities_all_comments_count['city_name'].tolist()
    y_axis = cities_all_comments_count['count'].tolist()
    ax = cities_all_comments_count.plot(kind='bar', color='blue')
    fig = ax.get_figure()
    ax.set_xticklabels(x_axis)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=70)
    ax.legend_.remove()
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + ylabel + '.png', dpi=200)
