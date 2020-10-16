import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

raw_df = pd.read_table('t9_hg19.txt', sep='\t', header=10)
# raw_df = pd.read_table('t9_hg38.txt', sep='\t', header=11)

raw_df = raw_df.drop_duplicates(subset=['Uploaded Variation'])

gene_list = raw_df['Gene'].dropna().unique().tolist()

frames = []

gene_dict = {}
cons_dict = {}


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


for gene in gene_list:
    subset_by(gene)

plot_ready = pd.concat(frames)

print(plot_ready)

# wrangle the dataframe for a stacked bar plot
plot_ready = plot_ready.groupby(['Gene', 'Consequence']).sum().unstack()

order = ['KNOP1', 'C16orf62', 'IQCK']

plot_ready.loc[order].plot(kind='barh', y='Num', stacked=True, cmap='Set3')

# extras # fontdict=dict(weight='bold')
plt.title('Chr16: 19,716,456-19,858,467', fontsize=25)
plt.xlabel('Number of Variant Annotations (#)', fontsize=20)
plt.ylabel('Gene', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=23, title='VAI Consequence',
           loc='lower right').get_title().set_fontsize('20')
plt.show()
