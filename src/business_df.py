import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 14})


class BusinessDF(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)
        self.stars_col = 'stars'
        self.review_count_col = 'review_count'


    def plot_value_counts_bar(self, col_name, filter_by=(), save=False):
        ''' 
        Plot a bar chart of the counts of each value in the specified column (limited to 10 top values).

        Parameters:
            col_name (string): Name of a categorical column in the dataframe to plot the counts of values.
            filter_by (tuple): Used to filter the data for plotting, e.g., filter_by=('Restaurant', [True]) will
                only plot businesses where the Restaurant column=True.  First value of the filter_by tuple is the
                column name (string) to filter on; second value is a list of values to keep.
            save (boolean): If true, will save the figure as a png file in the images folder.
        '''

        if filter_by:
            col, vals = filter_by
            filtered = self[self[col].isin(vals)]
            legend_label = f'count of businesses where {col} is in {vals}'
        else:
            filtered = self
            legend_label = 'count of businesses'

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        data = filtered[col_name].value_counts()[0:10]
        labels = data.index
        N = len(labels)
        tick_locations = np.arange(N)
        
        ax.barh(tick_locations, data, label=legend_label)
        ax.set_yticks(ticks=tick_locations)
        ax.set_yticklabels(labels)
        ax.set_xlabel('number of businesses')
        ax.set_ylabel(f'{col_name}')
        title = f'Number of Businesses by {col_name}'
        ax.set_title(title)
        ax.legend()
        plt.gca().invert_yaxis()

        if save:
            fig.savefig(f'../images/{title}.png')
        

    def plot_stars_hist(self, view_by_col='', filter_by=(), limit=10, save=False):
        '''
        Plot histrograms of avg star ratings, one plot for each value of the view_by_col

        Parameters:
            view_by_col (string): name of column to segment the data; shows 1 plot for each value
            filter_by (tuple): Used to filter the data for plotting, e.g., filter_by=('Restaurant', [True]) will
                only plot businesses where the Restaurant column=True.  First value of the filter_by tuple is the
                column name (string) to filter on; second value is a list of values to keep.
            limit (int): Max number of plots to show (will show top x frequent unique values of view_by_col)
            save (boolean): If true, will save the figure as a png file in the images folder.
        '''

        if filter_by:
            col, vals = filter_by
            filtered = self[self[col].isin(vals)]
            legend_label = f'star ratings where {col} is in {vals}'
        else:
            filtered = self
            legend_label = 'star ratings'
        
        if view_by_col:
            labels = filtered[view_by_col].value_counts()[0:limit].index  # Get the top x most frequent values of the view_by_col
            num_plots = len(labels)
            fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8, 4 * num_plots))

            for idx, label in enumerate(np.array(labels)):
                data = filtered[filtered[view_by_col]==label]
                stars_data = data[self.stars_col]
                ax = axs[idx]
                ax.hist(stars_data, bins=8, label=legend_label)
                ax.set_xlabel('avg. star rating')
                ax.set_title(f'{label}')
                ax.legend()

            title = f'Star Ratings by {view_by_col}'

        else:
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            stars_data = filtered[self.stars_col]
            ax.hist(stars_data, bins=8)
            title = 'Star Ratings Overall'
            ax.set_title(title)

        plt.tight_layout(pad=2)

        if save:
            fig.savefig(f'../images/{title}.png')


    def plot_review_counts_hist(self, view_by_col='', filter_by=(), limit=10, cutoff=5000, save=False):
        ''' 
        Plot histrograms of review counts, one plot for each value of the view_by_col.

        Parameters:
            view_by_col (string): name of column to segment the data; shows 1 plot for each value
            filter_by (tuple): Used to filter the data for plotting, e.g., filter_by=('Restaurant', [True]) will
                only plot businesses where the Restaurant column=True.  First value of the filter_by tuple is the
                column name (string) to filter on; second value is a list of values to keep.
            limit (int): Max number of plots to show (will show top x frequent unique values of view_by_col)
            cutoff (int): Only include businesses with fewer reviews than the cutoff in the plot, for viewability.
            save (boolean): If true, will save the figure as a png file in the images folder.
        '''
        cutoff_data = self[self[self.review_count_col] < cutoff]

        if filter_by:
            col, vals = filter_by
            filtered = cutoff_data[cutoff_data[col].isin(vals)]
            legend_label = f'review counts where {col} is in {vals}'
        else:
            filtered = self
            legend_label = 'review counts'
        
        if view_by_col:
            labels = filtered[view_by_col].value_counts()[0:limit].index  # Get the top x most frequent values of the view_by_col
            num_plots = len(labels)
            fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8, 4 * num_plots))

            for idx, label in enumerate(np.array(labels)):
                data = filtered[filtered[view_by_col]==label]
                review_count_data = data[self.review_count_col]
                ax = axs[idx]
                ax.hist(review_count_data, bins=20, label=legend_label)
                ax.set_xlabel('review counts')
                ax.set_title(f'{label}')
                ax.legend()

            title = f'Review Counts by {view_by_col}'

        else:
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            review_count_data = filtered[self.review_count_col]
            ax.hist(review_count_data, bins=20)
            title = 'Review Counts Overall'
            ax.set_title(title)

        plt.tight_layout(pad=2)

        if save:
            fig.savefig(f'../images/{title}.png')


if __name__ == '__main__':
    businesses_df = pd.read_pickle('../data/pickled_businesses_df')