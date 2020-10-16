import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('fivethirtyeight')

# read in data
raw_df = pd.read_csv('t31.csv', sep=',', header=0)

# data wrangling
raw_df['P'] = -np.log10(raw_df['P'])
raw_df['FDR P'] = -np.log10(raw_df['FDR P'])
subset_df = raw_df[raw_df['Trait'] != 'Alzheimers disease']
subset_df = subset_df[subset_df['Trait'] !=
                      'Illnesses of mother: Alzheimers disease/dementia']

# set p-value cut off for labelling
cutoff_df = subset_df[subset_df['P'] > 1.8]
trait_list = cutoff_df['Trait'].dropna().unique().tolist()

# main plot
plt.scatter(subset_df['rg'], subset_df['P'],
            c=subset_df['FDR P'], cmap='viridis')

def anot(trait):
    plt.annotate('{}'.format(
        trait), (cutoff_df['rg'][cutoff_df['Trait'] == trait], cutoff_df['P'][cutoff_df['Trait'] == trait]), fontsize=10)

plt.plot(cutoff_df['rg'], cutoff_df['P'], 'o', color='magenta',
         markeredgecolor='white', markeredgewidth=1, alpha=0.1)

# label points above p-value cut off
for trait in trait_list:
    anot(trait)


# extras
plt.axvline(x=0, c='k', lw=0.5, ls='-')
plt.axhline(y=-np.log10(0.05), c='r', lw=1, ls='--', label='0.05')
# plt.legend()
plt.colorbar(label=r'-log$_{10}$(FDR p-value)', orientation='vertical')
plt.xlabel('Correlation with Alzheimer\'s disease ', fontsize=20)
plt.ylabel(r'-log$_{10}$(correlation p-value)', fontsize=20)
plt.show()
