import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 14})


def plot_barh(x, y, title='', x_label='', y_label='', legend_label='', save=False):
    fig, ax = plt.subplots()
    ax.barh(x, y)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    plt.gca().invert_yaxis()
    if save:
        fig.savefig(f'../images/{title}.png')


if __name__ == '__main__':
    #Load the pickeled dataframes
    businesses_df = pd.read_pickle('../data/pickled_businesses_df')
    category_counts = pd.read_pickle('../data/pickled_category_counts')

    # Plot top 10 category frequency counts
    x = category_counts['elem'][0:10]
    y = category_counts['count'][0:10]
    title('Top 10 business categories')
    plot_barh(x, y, title=title, save=True)

    # Plot overall star ratings hist
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