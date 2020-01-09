# Yelp-Reviews
Capstone 1 project analyzing yelp user, review and business data

## Background / Context

## Data

.json files -- too big to go into GitHub

Businesses:
192,609 businesses
Across 10 metro areas in the US and Canada... 1258 distinct city, state combinations

Subsetted businesses to ones with at least 100 reviews.  N = 13,124

Reviews:
Flat schema (every field is at top level)

Users:
Pretty flat, other than "elite" : array of ints (years user was elite). Could get count of years elite and/or most recent year
                        "friends" : array of strings with user ids. Maybe just do a count of friends

NOTES ON BUSINESSES SCHEMA:
All attributes are strings.  Some, like 'AcceptsInsurance' are values True, False, None or null.
Some like AgesAllowed, Alcohol, are categories:


But then some like Ambience, BusinessParking, etc. are strings that look like dictionaries:





## Getting a sense of the businesses in the dataset - type, locations, # reviews

<div style="text-align:center"><img src="images/Top 10 business categories.png" /></div>

<div style="text-align:center"><img src="images/Review Counts for Businesses.png" /></div>

<div style="text-align:center"><img src="images/Number of Businesses by city.png" /></div>

<div style="text-align:center"><img src="images/10_metro_areas_heatmap.png" /></div>


## Looking at average star ratings

<div style="text-align:center"><img src="images/Avg. Star Ratings for Businesses.png" /></div>

<div style="text-align:center"><img src="images/Star Distributions by city.png" /></div>

<div style="text-align:center"><img src="images/Avg. Star Ratings of Restaurant vs. Other business types.png" /></div>


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


user_id, average_stars, elite, review_count, yelping_since




REVIEWS:
ids, stars, text, date



First review
+-------------------+
|          min(date)|
+-------------------+
|2004-10-12 10:13:32|
+-------------------+

Most recent review:
+-------------------+
|          max(date)|
+-------------------+
|2018-11-14 18:13:26|
+-------------------+

## Initial Observations

## Methods



## Future Analysis
