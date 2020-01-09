# Yelp-Reviews

<div style="text-align:center"><img src="images/Yelp_dataset.png" /></div>

<div style="text-align:center"><img src="images/Yelp_dataset_mini.png" /></div>

## Project Question / Goal

Rating websites that allow users to provide numerical ratings of movies, restaurants, products, etc. can be helpful to consumers, however often times the ratings seem to center around a certain number, e.g., 

Yelp.com is a website that allows people to give a star rating of 1-5 for local businesses they've visited - including restaurants, shops, bars, mechanics, etc.  As a frequent user and contributer on Yelp.com, I'm interested in the distribution of these ratings, and how they may vary across cities, types of businesses, users, etc.  It seems that ratings tend to center around ~4 stars, and most businesses have an average star rating of 3.5 to 4.5 stars.

I'm also interested to see if types of businesses vary b

Yelp provides <a href="https://www.yelp.com/dataset">an open dataset</a> for academic/research purposes, available as downloadable .json files.  It includes a subset of Yelp businesses, reviews, users, photos, "tips", and "check-ins" across 10 metro areas in the U.S. and Canada, over the years 2004-2014.  For this project, I focused on the businesses and users data, investigating average star ratings and review counts across various attributes of the businesses.


## Data Description

The Yelp data is provided in .json files, one file each for businesses, users, and reviews.  There are 192,609 businesses and 1,637,138 users.  I initially wanted to also include the review data in my analysis (6M+ reviews), but for this exploratory data analysis project I excluded it.

The users data schema (in json) was flat, however the businesses schema included heirarchial structures for the attributes that needed to be flattened in order to work with them efficiently.  Also, the 'categories' column for businesses lists all of the categories that apply to a business (e.g., one business could have Restaurant, Chinese, Bar, etc.) so to get the top most frequently used categories I had to split these out.  The json files were read into Spark dataframes.

Lastly, I subsetted the businesses and user data to only businesses with at least 100 reviews and only users with at least 200 reviews.  I used this as a proxy to look at 'established' businesses and frequent Yelp users, and also served to reduce the size of the data frames so they could be converted to pandas.  This left me with 13,124 businesses and 30,788 users.


## Exploratory Data Analysis

For this EDA project, I wanted to look primarily at the distribution of star ratings for different business and user attributes.  Every business and user has an "average star rating" that is the average of all ratings for that business/user.  Since I only included businesses and users with a substantial number of reviews, these average ratings should be representative for the business/user, and not include, for example, a 2-star business with only five reviews.


## Overview of the businesses

I started out by getting a picture of the businesses in the dataset, including locations, types of businesses, number of reviews for each, etc.

This chart shows the top 10 most frequent categories for the businesses.  Unsurprisingly, 'Restaurant' is by far the most frequent category, followed by 'Food', 'Nightlife' and 'Bar'.  Remember that a business can be assigned multiple categories, and many businesses fall into multiple categories.

<div style="text-align:center"><img src="images/Top 10 business categories.png" /></div>

Next I looked at the number of reviews each business has.  Since I only included businesses with at least 100 reviews, businesses with fewer than this (which is the large majority of businesses in the original dataset) are not shown.  Also, you can see that the number of reviews per business falls off very sharply, with few businesses having more than 500 reviews.

<div style="text-align:center"><img src="images/Review Counts for Businesses.png" /></div>

Lastly in the initial overview, I wanted to see what were the 10 metro areas included in the dataset.  The first chart shows the top ten cities in the dataset -- note that a metro area may include multiple cities, e.g., Henderson is part of the Las Vegas metro area and Scottsdale is near Phoenix.

<div style="text-align:center"><img src="images/Number of Businesses by city.png" /></div>

To see all of the metro areas geographically, I made a heatmap of the businesses.

<div style="text-align:center"><img src="images/10_metro_areas_heatmap.png" /></div>


## Looking at average star ratings

Next, I looked at the average star rating distributions for the businesses.  A business' average star rating is given in half-stars (1.0, 1.5, 2.0, 2.5, etc.).  Not surprisingly, the average ratings center around 4, with very few having an average rating of 3 or less.

<div style="text-align:center"><img src="images/Avg. Star Ratings for Businesses.png" /></div>

Next, I compared the average ratings of restaurants to other 'non-restaurant' types of businesses.  This does show variation in the ratings distributions, with many more "other" businesses having 4.5 and 5-star ratings.  From my experience on Yelp.com, I do this pattern -- a flower shop or mechanic is more likely to have a 5-star rating, while restaurants seem to be mostly in the range of 3.5 to 4.5 stars.

<div style="text-align:center"><img src="images/Avg. Star Ratings of Restaurant vs. Other business types.png" /></div>

Then I looked at the star ratings by city (for the top 5 cities with the most businesses).  This also shows variation, with Phoenix and Las Vegas having higher average ratings, and Toronto having substantially lower ratings.  In a future analysis, it may be interesting to compare other aspects of these cities (sunshine index, happiness, # of tourists vs. locals, income) to see if any of these variables may be associated with the variation in yelp ratings.

<div style="text-align:center"><img src="images/Star Distributions by city.png" /></div>

Finally, I looked how the number of reviews for a buiness is associated with its average star rating.  This chart shows that the businesses with the most reviews have ratings between 2.5 and 4.5 stars, and that the more reviews a business gets, the more it tends towards 3.5-4 star average (the mean of the averages is 3.77).

<div style="text-align:center"><img src="images/Avg. Star Rating vs. Number of Reviews.png" /></div>


If you want to use your bitcoin, go to Vegas.
<div style="text-align:center"><img src="images/Businesses that Accept Bitcoin by City.png" /></div>


## Mapping businesses
<div style="text-align:center"><img src="images/vegas_businesses_heatmap.png" /></div>

<div style="text-align:center"><img src="images/Charlotte_businesses.png" /></div>

# USERS

USERS:
1637138 users

If we only look at users with at least 200 reviews, this decreases the number of users to 30788.


## Average star rating distribution

<div style="text-align:center"><img src="images/User Avg. Star Ratings.png" /></div>

## Review counts distribution

<div style="text-align:center"><img src="images/User Review Counts.png" /></div>




## Future Analysis
