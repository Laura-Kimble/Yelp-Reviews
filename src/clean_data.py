'''
Functions and code to import .json files to spark dataframes,
flatten .json schema into flat dataframe files,
and convert to pandas dataframes.

Do this for the Yelp data files: businesses, reviews, and users.
'''

import pyspark as ps
import json as js
import pyspark.sql.functions as F
from pyspark.sql.types import *
import pandas as pd
import business_df as bd

def set_up_spark_env(appname):
    ''' 
    Set up spark environment and return the spark session and context.
    '''

    spark = (ps.sql.SparkSession.builder 
        .master("local[4]") 
        .appName(appname) 
        .getOrCreate()
        )
    sc = spark.sparkContext
    return spark, sc


def read_json_to_df(filename):
    '''
    Read in .json file, convert to a spark dataframe.

    Parameters: 
        filename (str): Path and name to .json file

    Returns:
        A spark dataframe
    '''

    # rdd = sc.textFile(filename)
    df = spark.read.json(filename)
    # df.createOrReplaceTempView(df_name)

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

# Need to clean up some fields in the flat df... nulls, 'True'/'False' strings to boolean..
# Ambience, BusinessParking, etc, are still stored as strings that look like dicts in a single col: {'romantic': False, 'classy':...}

if __name__ == '__main__':
    spark, sc = set_up_spark_env('yelp_review_analysis')

    # Read in json files and flatten the businesses df
    business_df = read_json_to_df('../../data/yelp_dataset/business.json')
    business_df_flat = flatten_df(business_df)
    business_df_flat_subset = subset_businesses(business_df_flat, 100)

    user_df = read_json_to_df('../../data/yelp_dataset/user.json')

    review_df = read_json_to_df('../../data/yelp_dataset/review.json')
    review_df = review_df.withColumn('date', F.to_date(review_df.date, 'yyyy-MM-dd'))

    # Convert spark df's to pandas df's for plotting
    businesses = business_df_flat_subset.select('*').toPandas()
    # users = user_df.select('*').toPandas()
    # reviews = review_df.select('*').toPandas()


    businesses_df = bd.BusinessDF(businesses)
    businesses_df['Restaurant'] = businesses_df['categories'].str.contains(pat='Restaurant')

