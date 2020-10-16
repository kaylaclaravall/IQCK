import pandas as pd
import matplotlib.pyplot as plt

# matplotlib theme
plt.style.use('fivethirtyeight')

# read in UCSC VAI results
raw_df = pd.read_table('t9_hg19.txt', sep='\t', header=10)

# remove duplicate annotations of the same variant
raw_df = raw_df.drop_duplicates(subset=['Uploaded Variation'])

# create a list containing the gene names with no duplicates
gene_list = raw_df['Gene'].dropna().unique().tolist()

# set up frames
frames = []

# gene dictionary
gene_dict = {}
# consequence dictionary
cons_dict = {}

# define function
def subset_by(gene):
    #
    global gene_dict, cons_dict
    #
    gene_dict['{}'.format(gene)] = raw_df[raw_df['Gene'] == gene]
    #
    cons_dict['{}'.format(gene)] = gene_dict[gene].groupby(
        'Consequence')[['Consequence']].count()
    #
    cons_dict[gene].rename(columns={'Consequence': 'Num'}, inplace=True)
    cons_dict[gene]['Gene'] = gene
    #
    frames.append(cons_dict[gene])

# run function for each gene in gene_list
for gene in gene_list:
    subset_by(gene)

# concat all the dfs in 'frames' into one df
plot_ready = pd.concat(frames)

# wrangle the dataframe for a stacked bar plot
plot_ready = plot_ready.groupby(['Gene', 'Consequence']).sum().unstack()

# define order of bars
order = ['KNOP1', 'C16orf62', 'IQCK']

# main plot
plot_ready.loc[order].plot(kind='barh', y='Num', stacked=True, cmap='Set3')

# extras
plt.title('Chr16: 19,716,456-19,858,467', fontsize=25)
plt.xlabel('Number of Variant Annotations (#)', fontsize=20)
plt.ylabel('Gene', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=23, title='VAI Consequence',
           loc='lower right').get_title().set_fontsize('20')
plt.show()
