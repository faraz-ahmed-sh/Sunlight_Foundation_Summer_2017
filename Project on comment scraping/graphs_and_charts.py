import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
GRAPHS AND CHARTS
'''

def sentimental_analysis_charts(list_, option):
    
    if option == "both":
        
    
        #chart 1: for the count of comments
        fig = plt.figure()
        x_objects = [i for i in list_[:6] if type(i) == str]
        y_pos = np.arange(len(x_objects))
        y_objects = [i for i in list_[:6] if type(i) == int]

        plt.bar(y_pos, y_objects, align='center', alpha=0.7, color="red")
        plt.xticks(y_pos, x_objects)
        plt.ylabel('Count of comments')
        plt.title('Sentiment Analysis Count -' + " " + list_[-4], weight="bold")
        plt.tight_layout()
        plt.show()
        fig.savefig('sentiment-count-' + list_[-4] + '.png', dpi = 200)
        
        #return list_
    
    elif option == "tot_sent":
    
        # Chart 3 for the count of total sentences

        x_objects = ['Buffalo', 'Durham', 'Tyler', 'Glendale', 'Nashville', 'Syracuse', 'Naperville', 'Bart', 
                    'San Francisco']

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
        fig.savefig('fig1.png', dpi = 200)


def horizontal_bar(x_objects, y_objects, xlabel, title):
    
    fig = plt.figure()
    y_pos = np.arange(len(x_objects))
    
    plt.barh(y_pos, y_objects, align='center', alpha=0.7, color="brown")
    plt.xticks(y_objects)
    plt.yticks(y_pos, x_objects)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    fig.savefig(title + '.png', dpi = 200)


def pie_chart(sizes, labels, savefigcaption):
    '''
    For proportion of positive, negative and neutral comments.
    '''

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, autopct='%1.1f%%',
            shadow=True, startangle=90, pctdistance=1.125)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(labels, loc="upper corner")
    plt.tight_layout()
    plt.show()
    fig1.savefig(savefigcaption + '.png', dpi = 200)


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
    

def likes_replies_chart(ylabel, title, likes_x, likes_y, replies_x, replies_y, dictionaries):
    '''
    For likes/replies
    '''
    
    likes_x, likes_y, replies_x, replies_y = transform_likes_replies(likes_x, likes_y, replies_x, replies_y, dictionaries)

    N = 9
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
    ax.legend((rects1[0], rects2[0]), ('Likes', 'Replies'))
    

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
    fig.savefig('fig-likes-replies.png', dpi = 200)