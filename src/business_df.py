import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class BusinessDF(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)


    def plot_hist(self, col_name, view_by_col=''):
        ''' Plot histrograms of the given col_name, one for each value of the view_by_col
        '''
        if view_by_col:
            num_plots = len(self[view_by_col].unique())
            fig, axs = plt.subplots(num_plots, 1, figsize=(10, 4))

            for idx, val in enumerate(self[view_by_col].unique()):
                data = self[self[view_by_col]==val][col_name]
                ax = axs[idx]
                ax.hist(data, label=f'{view_by_col} = {val}')
                ax.set_title(f'{col_name}')
                ax.legend()

        else:
            fig, ax = plt.subplots(1, 1, figsize=(4, 8))
            ax.hist(self[col_name], label=f'{col_name}')
            ax.legend()

        plt.tight_layout()


if __name__ == '__main__':
    businesses = BusinessDF(businesses)