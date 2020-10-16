import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# matplotlib set up
plt.style.use('seaborn-talk')

# read in table 11
raw_df = pd.read_csv('t11.csv', sep=',', header=0)
# subset by IQCK locus
subset_df = raw_df[raw_df['Locus'] == 'IQCK']


# data transformation
subset_df['logP'] = np.log10(subset_df['Stage 1 P-value'])
subset_df['logP'] = -subset_df['logP']
subset_df['Pos'] = subset_df['Pos'] / 1000000

# define lead variant
lead_var = subset_df[subset_df['rsID'] == 'rs7185636']

# main plot
plt.scatter(subset_df['Pos'], subset_df['logP'],
            c=subset_df['R2'], cmap='jet', s=100, vmin=0, vmax=1)

# label lead variant only
plt.plot(lead_var['Pos'], lead_var['logP'], marker='D',
         color='magenta', markeredgecolor='white', markeredgewidth=1)
plt.annotate('rs7185636', (lead_var['Pos'], lead_var['logP']))

# extras
plt.ticklabel_format(style='plain')
plt.colorbar(label=r'r$^2$', orientation='vertical')
plt.xlabel('Chr16 nucleotide position (Mbp)', fontsize=20)
plt.ylabel(r'-log$_{10}$(p-value)', fontsize=20)
plt.show()
