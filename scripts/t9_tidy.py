import pandas as pd
import matplotlib.pyplot as plt

# matplotlib set up
plt.style.use('fivethirtyeight')


# read in table 9
raw_df = pd.read_csv('t9.csv', sep=',', header=2)

# subset by IQCK locus
subset_df = raw_df[raw_df['LOCUS'] == 'IQCK']

# count how many times each gene symbol pops up
genes_count = subset_df.groupby('Gene Symbol')['Gene Symbol'].count()

# gather the gene names into a list
gene_list = genes_count.index.tolist()


# scrape table from ensembl.org
url = 'https://m.ensembl.org/info/genome/variation/prediction/predicted_data.html'
raw_table = pd.read_html(url, header=0)[0]

# gather the VEP consequences into a list
vep_list = raw_table['SO term'].tolist()


# using the names of the VEP consequences, subset the dataframe according to those names
# end up with a 'dictionary' of dataframes, one for each VEP name.
d = {}
for i in vep_list:
    d['{}'.format(i)] = subset_df[subset_df['VEP Consequence'].str.contains(
        i, case=False)]

# for each VEP dataframe, count how many times each gene symbol pops up
vep_dict = {}
for i in d:
    vep_dict['{}'.format(i)] = d[i].groupby(
        'Gene Symbol')['Gene Symbol'].count()


# define the rows of a new dataframe
data = []
for df_name in vep_dict:
    for gene_name in gene_list:
        if gene_name in vep_dict[df_name]:
            data.append([gene_name, df_name, vep_dict[df_name][gene_name]])
        else:
            pass

# define the columns of the new dataframe
df = pd.DataFrame(data, columns=['Gene Symbol', 'VEP Consequence', 'Num'])


# wrangle the dataframe for a stacked bar plot
plot_ready = df.groupby(['Gene Symbol', 'VEP Consequence']).sum().unstack()

# plot
plot_ready.plot(kind='barh', y='Num', stacked=True, cmap='Set3')

# extras # fontdict=dict(weight='bold')
plt.title('IQCK locus (chr16:19808163)', fontsize=25)
plt.xlabel('Number of Variants Discovered (#)', fontsize=20)
plt.ylabel('Gene', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=23, title='VEP Consequence').get_title().set_fontsize('20')
plt.show()
