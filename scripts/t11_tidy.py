import pandas as pd
import matplotlib.pyplot as plt

# matplotlib set up
plt.style.use('fivethirtyeight')

# read in table 11
raw_df = pd.read_csv('t11.csv', sep=',', header=0)
# subset by IQCK locus
subset_df = raw_df[raw_df['Locus'] == 'IQCK']
# keep entries without NA for the "feature" column
subset_df = subset_df[subset_df['Ensembl Regulatory Build Feature'].notna()]

# subset_df['Ensembl Regulatory Build Feature'] = subset_df['Ensembl Regulatory Build Feature'].fillna('-')


# gather the remaining gene names into a list
gene_list = subset_df['Ensembl Overlapped Gene'].tolist()
# remove duplicates in list
gene_list = list(dict.fromkeys(gene_list))



# gather feature names into a list
feat_list = subset_df['Ensembl Regulatory Build Feature'].tolist()
# remove duplicates in list
feat_list = list(dict.fromkeys(feat_list))



# subset dataframe according to gene names
# end up with a dataframe for each gene name
gene_dict = {}
for i in gene_list:
	gene_dict['{}'.format(i)] = subset_df[subset_df['Ensembl Overlapped Gene'] == i]



# for each gene dataframe, count how many times each "feature" pops up
feat_dict = {}
for i in gene_dict:
	feat_dict['{}'.format(i)] = gene_dict[i].groupby('Ensembl Regulatory Build Feature')['Ensembl Regulatory Build Feature'].count()


# define the rows of a new dataframe
data = []
for df_name in feat_dict:
	for feat in feat_list:
		if feat in feat_dict[df_name]:
			data.append([df_name, feat, feat_dict[df_name][feat]])

# define the columns of the new dataframe
df = pd.DataFrame(data, columns=['Gene', 'Ensembl Regulatory Build Feature', 'Num'])



# wrangle the dataframe for a stacked bar plot
plot_ready = df.groupby(['Gene', 'Ensembl Regulatory Build Feature']).sum().unstack()
# plot
plot_ready.plot(kind='barh', y='Num', stacked=True, cmap='Set3')

# extras
plt.title('IQCK locus (chr16:19808163)', fontsize=25)
plt.xlabel('Number of Regulatory Variants (#)', fontsize=20)
plt.ylabel('Gene', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=23, title='Ensembl Regulatory Build Feature').get_title().set_fontsize('20')
plt.show()
