import pyspark as ps
import json as js
import pyspark.sql.functions as F
from pyspark.sql.types import *
import pandas as pd
import business_df as ydf

def set_up_spark_env(appname):
    ''' Set up spark environment and return the spark session and context.'''

    spark = (ps.sql.SparkSession.builder 
        .master("local[4]") 
        .appName(appname) 
        .getOrCreate()
        )
    sc = spark.sparkContext
    return spark, sc


def read_json_to_df(filename):
    '''Read in .json file, convert to a spark dataframe.'''

    df = spark.read.json(filename)
    return df
    

def flatten_df(nested_df):
    '''
    Flatten a nested dataframe where some columns are nested structures.

    Parameters:
        nested_df (spark dataframe): Dataframe with nested columns

    Returns:
        flat_df (spark dataframe): Dataframe that includes a column for each element under a nested structure
    '''

    new_col_names = []
    columns = nested_df.dtypes
    for col in columns:
        col_name = col[0]
        col_type = col[1].strip('>').split('<')  # If the column type is a structure, we want to split it into the 'struct' then the underlying schema
        if col_type[0] == 'struct':  # If the column type is a structure
            nested_cols = col_type[1].split(',')
            nested_col_names = [col.split(':')[0] for col in nested_cols]
            nested_col_refs = ['.'.join([col_name, name]) for name in nested_col_names]
            new_col_names.extend(nested_col_refs)
        else:
            new_col_names.append(col_name)

    flat_df = nested_df.select(new_col_names)
    return flat_df


def subset_businesses(df, n=100):
    ''' Subset the businesses dataframe to only businesses with at least n reviews.'''
    
    subset_df = df.filter(df.review_count >= n)
    return subset_df


def subset_users(user_df, n=50):
    ''' Subset the users df to only users with at least n reviews.'''

    subset_df = user_df.filter(user_df.review_count >= n)
    return subset_df


def get_counts_in_string_col(df, col_name):
    ''' Take a column in a df that is a string of words separated by commas
    (e.g., 'categories' column might have a row that is 'Restaurant, Chinese, Food'),
    and convert the column to a list of words, and then get a frequency count for each word in the dataframe.
    '''
    df_col = df.select(df[col_name].alias('string_col'))
    df_col.createOrReplaceTempView('df_col')
    df_list_col = spark.sql('''
                        SELECT split(string_col, ',') as lst_col
                        FROM df_col
                            ''')

    df_list_col.createOrReplaceTempView('df_list_col')

    elements = spark.sql('''
                        SELECT trim(elem) as elem
                        FROM df_list_col
                        LATERAL VIEW explode(lst_col) as elem
                        ''')

    counts_df = get_counts(elements, 'elem')
    return counts_df


def get_counts(df, col_name):
    return df.groupBy(df[col_name]).count().orderBy('count', ascending=False)


# Need to clean up some fields in the flat df... nulls, 'True'/'False' strings to boolean..
# Ambience, BusinessParking, etc, are still stored as strings that look like dicts in a single col: {'romantic': False, 'classy':...}

if __name__ == '__main__':
    spark, sc = set_up_spark_env('yelp_review_analysis')

    # Read in json files and flatten the businesses df
    business_df = read_json_to_df('../../data/yelp_dataset/business.json')
    business_df_flat = flatten_df(business_df)
    business_df_flat_subset = subset_businesses(business_df_flat, 100)
    category_counts = get_counts_in_string_col(business_df_flat_subset, 'categories')

    user_df = read_json_to_df('../../data/yelp_dataset/user.json')
    user_df_subset = subset_users(user_df, 300)

    # review_df = read_json_to_df('../../data/yelp_dataset/review.json')
    # review_df = review_df.withColumn('date', F.to_date(review_df.date, 'yyyy-MM-dd'))

    # Convert spark df's to pandas df's for plotting
    businesses = business_df_flat_subset.select('*').toPandas()
    category_counts = category_counts.select('*').toPandas()
    users = user_df_subset.select('*').toPandas()
    # reviews = review_df.select('*').toPandas()

    #businesses_df = ydf.YelpDF(businesses, 'stars', 'review_count')
    businesses_df['Restaurant'] = businesses_df['categories'].str.contains(pat='Restaurant')

    #users_df = ydf.YelpDF(users, 'average_stars', 'review_count')

    # save to pickle files
    businesses_df.to_pickle('../data/pickled_businesses_df')
    category_counts.to_pickle('../data/pickled_category_counts')
    users_df.to_pickle('../data/pickled_user_df')

