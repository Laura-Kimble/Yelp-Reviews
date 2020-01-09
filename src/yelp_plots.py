import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import business_df as ydf
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 14})


def plot_barh(x, y, title='', x_label='', y_label='', legend_label='', save=False):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.barh(x, y)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    plt.gca().invert_yaxis()
    plt.tight_layout(pad=2)
    if save:
        fig.savefig(f'../images/{title}.png')


def plot_stars_violin(df, label_col, label_names, save=False):

    data = [np.array(df[df[label_col]==lab]['stars']) for lab in label_names]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.violinplot(data, vert=False, widths=0.8)
    ax.set_yticks(np.arange(1, len(label_names) + 1))
    ax.set_yticklabels(label_names)

    title = f'Star Distributions by {label_col}'
    ax.set_title(title)
    fig.tight_layout(pad=1)
    if save:
        fig.savefig(f'../images/{title}.png')


if __name__ == '__main__':
    #Load the pickeled dataframes and convert to YelpDF's to use the class plotting functions
    businesses_df = pd.read_pickle('../data/pickled_businesses_df')
    businesses_df = ydf.YelpDF(businesses_df, 'stars', 'review_count')

    category_counts = pd.read_pickle('../data/pickled_category_counts')

    users_df = pd.read_pickle('../data/pickled_user_df')
    users_df = ydf.YelpDF(users_df, 'average_stars', 'review_count')

    # Plot top 10 category frequency counts
    x = category_counts['elem'][0:10]
    y = category_counts['count'][0:10]
    title = 'Top 10 business categories'
    plot_barh(x, y, title=title, save=True)

    # Violin plots for businesses
    top_5_cities = businesses_df['city'].value_counts()[0:5].index
    plot_stars_violin(businesses_df, 'city', top_5_cities, save=False)
    plot_stars_violin(businesses_df, 'Restaurant', [True, False], save=True)

    # Plot histograms for users
    users_df.plot_stars_hist(save=True)
    users_df.plot_review_counts_hist(cutoff=2000, save=True)

    # Plot average star ratings hist for businesses
    ax = businesses_df['stars'].hist(bins=8)
    ax.set_title('Average Star Rating: Distribution for All Businesses')
    ax.set_xlabel('avg. stars')
    ax.set_ylabel('count of businesses')

    fig = ax.figure
    fig.set_size_inches(8, 5)
    fig.tight_layout(pad=1)
    fig.savefig('../images/Overall_stars_hist.png')


    # Plot overall review counts histogram.
    cutoff = 2000   # Only include businesses with fewer than this many reviews
    data = businesses_df[businesses_df['review_count'] < cutoff]['review_count']
    ax = data.hist(bins=20)
    ax.set_title('Review Counts: All Businesses')
    ax.set_xlabel('review count')
    ax.set_ylabel('count of businesses')
    ax.set_xlim(0, cutoff)

    fig = ax.figure
    fig.set_size_inches(8, 5)
    fig.tight_layout(pad=1)
    fig.savefig('../images/Overall_reviewCounts_hist.png')


    # Scatter plot of the average star rating vs. number of reviews (for businesses with between 100-5000 reviews)
    fig, ax = plt.subplots()
    data = businesses_df[businesses_df['review_count']<5000]
    x = data['stars']
    y = data['review_count']
    ax.scatter(x, y)
    ax.set_xlabel('avg star rating')
    ax.set_ylabel('number of reviews')
    title = 'Avg. Star Rating vs. Number of Reviews'
    ax.set_title(title)
    plt.tight_layout(pad=2)
    fig.savefig(f'../images/{title}.png')


    # Plot count of businesses that accept bitcoin, by city
    col_name = 'city'
    col, vals = ('BusinessAcceptsBitcoin', ['True'])
    filtered = businesses_df[businesses_df[col].isin(vals)]
    legend_label = f'count of businesses where {col} is in {vals}'

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    data = filtered[col_name].value_counts()[0:10]
    labels = data.index
    N = len(labels)
    tick_locations = np.arange(N)

    restaurant_counts = []
    non_restaurant_counts = []

    for lab in labels:
        restaurant_data = filtered[(filtered['Restaurant']==True) & (filtered[col_name]==lab)]
        non_restaurant_data = filtered[(filtered['Restaurant']==False) & (filtered[col_name]==lab)]
        restaurant_counts.append(len(restaurant_data))
        non_restaurant_counts.append(len(non_restaurant_data))
            
    ax.barh(tick_locations, restaurant_counts, label='Restaurants')
    ax.barh(tick_locations, non_restaurant_counts, label='Not Restaurants', left=restaurant_counts)
    ax.set_yticks(ticks=tick_locations)
    ax.set_yticklabels(labels)
    ax.set_xticks(np.arange(0, max(restaurant_counts) + max(non_restaurant_counts) + 1, step=5))
    ax.set_xlabel('number of businesses')
    ax.set_ylabel(f'{col_name}')
    title = f'Businesses that Accept Bitcoin by {col_name}'
    ax.set_title(title)
    ax.legend()
    plt.gca().invert_yaxis()
    fig.savefig(f'../images/{title}.png')