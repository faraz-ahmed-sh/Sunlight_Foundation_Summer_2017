import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import numpy as np


def read_data(filename1):
    '''
    This function reads the filename and puts the data into a dataframe.
    
    input: the name of the file
    output: a dataframe    
    '''
    
    df = pd.read_csv(filename1 + '.csv', header=None, index_col=False, encoding = "ISO-8859-1")
    return df

def duplicate_values_dictionary(df):

	m_cities = {}
	for city in df.values:
	    
	    if city[0] in m_cities:
	        m_cities[city[0]].append(city[1])
	        m_cities[city[0]].append(city[2])
	        
	    else:
	        m_cities[city[0]] = []
	        m_cities[city[0]].append(city[1])
	        m_cities[city[0]].append(city[2])

	return m_cities

def explore_analysis(column1, column2, option, df):
    '''
    This function returns three types of analysis (descriptive stats, groupby on mean, groupby on count) 
    give two columns of a dataframe.
    
    input:
        column1: the column for which we want statistics on a grouped data
        column2: the column on which grouping is performed
        
    output: 
        a dataframe with desired type of analysis    
    '''
    
    if option == 'describe':
        df_2 = df[column1].describe()
    elif option == 'groupby_mean':
        df_2 = df[column1].groupby(df[column2]).mean().reset_index()
    elif option == 'groupby_median':
        df_2 = df[column1].groupby(df[column2]).median().reset_index()
    elif option == 'groupby_count':
        df_2 = df[column1].groupby(df[column2]).count().reset_index()
    elif option == 'grouby_max':
        df_2 = df[column1].groupby(df[column2]).max().reset_index()
    
    return df_2


def seaborn_chart(x_1, y_1, data_1, xlabel_1, ylabel_1, title):
    '''
    This function returns a chart for two columns (x-axis and y-axis)
    '''
    
    sns.set_style("whitegrid")
    sns.set(font_scale = 1.25)
    ax = plt.subplots(figsize=(18, 5))
    ax = sns.barplot(x=x_1, y=y_1, data=data_1)

    ax.set(xlabel=xlabel_1)
    ax.set(ylabel=ylabel_1)    
    plt.title(title)
    plt.show()
    fig = ax.get_figure()
    fig.savefig('images/' + title + '.png', dpi=200)


def horizontal_bar_from_dataframe(df, yaxis, xaxis, xlabel):
    '''
    Makes a horizontal bar chart given a dataframe.
    '''

    all_categories = df[yaxis]
    ax = df[[xaxis]].plot(kind="barh")
    
    fig = ax.get_figure()
    ax.set_xlabel(xlabel)
    #ax.set_title('Who comments the most?')
    ax.set_yticklabels(all_categories)
    fig.tight_layout()
    ax.legend_.remove()
    plt.tight_layout()
    plt.show()
    fig.savefig('images/' + xlabel + '.png', dpi=200)


def vertical_bar_from_dataframe(df, xaxis, yaxis, ylabel):
	'''
	Makes a horizontal bar chart given a dataframe.
	'''

	x_axis = df[xaxis]
	ax = df[[yaxis]].plot(kind='bar', color='blue')
	fig = ax.get_figure()
	ax.set_xticklabels(x_axis)
	ax.set_ylabel(ylabel)
	plt.xticks(rotation=70)
	ax.legend_.remove()
	plt.tight_layout()
	plt.show()
	fig.savefig('images/' + ylabel + '.png', dpi=200)


def small_multiples_plots_for_duplicate_cities(multiple_cities):
	'''
	Makes small (multiple) plots of cities with multiple policies.
	'''

	fig = plt.figure(figsize = (11,8))

	fig.text(0.4, -0.02, 'Year', ha='center', fontsize=20)
	fig.text(-0.03, 0.5, 'Adoption Rate (median)', va='center', rotation='vertical', fontsize=20)

	font = {'weight' : 'medium', 'size'   : 5}
	plt.rc('font', **font)
	plt.subplots_adjust(hspace=.005)

	rows = 4
	cols = 4
	n = 1

	for city, values in multiple_cities.items():
	    plt.subplot(rows, cols, n)
	    plt.rc('xtick',labelsize=10)
	    plt.rc('ytick',labelsize=12)

	    plt.title(city, fontsize=15)
	    x=[]
	    y=[]
	    
	    for i in range(len(values)):
	        if i % 2 != 0:
	            y.append(values[i])
	        else:
	            x.append(values[i])
	    axes = plt.gca()
	    axes.set_ylim([0,1])
	    plt.xticks(x)	    
	    plt.plot(x, y, linewidth=1.5)
	    n += 1
	    
	    #plt.xlabel('Year', fontsize=15)
	    #plt.ylabel('Number of policies', fontsize=15)
	
	plt.tight_layout()
	plt.show()
	fig.savefig('images/' + 'multiple-policies-analysis' + '.png', dpi=200)
