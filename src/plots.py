import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 14})


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