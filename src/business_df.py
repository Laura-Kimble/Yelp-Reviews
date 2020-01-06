import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 14})


class BusinessDF(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)


    def plot_value_counts_bar(self, col_name, save=False):
        ''' 
        Plot a bar chart of the counts of each value in the specified column (limited to 10 top values).

        Parameters:
            col_name (string): Name of a categorical column in the dataframe to plot the counts of values.
            save (boolean): If true, will save the figure as a png file in the images folder.
        ''' 

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        data = self[col_name].value_counts()[0:10]
        labels = data.index
        N = len(labels)
        tickLocations = np.arange(N)
        
        ax.barh(tickLocations, data)
        ax.set_yticks(ticks=tickLocations)
        ax.set_yticklabels(labels)
        title = f'{col_name}: Value counts'
        ax.set_title(title)
        plt.gca().invert_yaxis()

        if save:
            fig.savefig(f'../images/{title}.png')
        

    def plot_stars_hist(self, view_by_col='', limit=10, save=False):
        '''
        Plot histrograms of avg star ratings, one plot for each value of the view_by_col

        Parameters:
            view_by_col (string): name of column to segment the data; shows 1 plot for each value
            limit (int): Max number of plots to show (will show top x frequent unique values of view_by_col)
            save (boolean): If true, will save the figure as a png file in the images folder.
        '''
        
        if view_by_col:
            labels = self[view_by_col].value_counts()[0:limit].index  # Get the top x most frequent values of the view_by_col
            num_plots = len(labels)
            fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8, 4 * num_plots))

            for idx, label in enumerate(np.array(labels)):
                data = self[self[view_by_col]==label]['stars']
                ax = axs[idx]
                ax.hist(data, bins=8, label=f'{view_by_col} = {label}')
                ax.set_xlabel('avg. star rating')
                ax.set_title(f'{label}')
                # ax.legend()

            title = f'Star Ratings by {view_by_col}'

        else:
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            ax.hist(self['stars'], bins=8)
            title = 'Star Ratings Overall'
            ax.set_title(title)

        plt.tight_layout(pad=2)

        if save:
            fig.savefig(f'../images/{title}.png')


    def plot_review_counts_hist(self, view_by_col='', limit=10, cutoff=5000, save=False):
        ''' 
        Plot histrograms of review counts, one plot for each value of the view_by_col.

        Parameters:
            view_by_col (string): name of column to segment the data; shows 1 plot for each value
            limit (int): Max number of plots to show (will show top x frequent unique values of view_by_col)
            cutoff (int): Only include businesses with fewer reviews than the cutoff in the plot, for viewability.
            save (boolean): If true, will save the figure as a png file in the images folder.
        '''
        cutoff_data = self[self['review_count'] < cutoff]
        
        if view_by_col:
            labels = cutoff_data[view_by_col].value_counts()[0:limit].index  # Get the top x most frequent values of the view_by_col
            num_plots = len(labels)
            fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(8, 4 * num_plots))

            for idx, label in enumerate(np.array(labels)):
                data = cutoff_data[cutoff_data[view_by_col]==label]['review_count']
                ax = axs[idx]
                ax.hist(data, bins=20, label=f'{view_by_col} = {label}')
                ax.set_xlabel('review counts')
                ax.set_title(f'{label}')
                # ax.legend()

            title = f'Review Counts by {view_by_col}'

        else:
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            ax.hist(cutoff_data['review_count'], bins=20)
            title = 'Review Counts Overall'
            ax.set_title(title)

        plt.tight_layout(pad=2)

        if save:
            fig.savefig(f'../images/{title}.png')


# if __name__ == '__main__':
#     businesses = BusinessDF(businesses)