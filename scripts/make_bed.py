import pandas as pd

# read in table 9
raw_df = pd.read_csv('t9.csv', sep=',', header=2)
subset_df = raw_df[raw_df['LOCUS'] == 'IQCK']

# set output file
outFileName = 'IQCK_variants.BED'
outFile = open(outFileName, 'w+')

# create bed_list
scaffold = 'NC_000016.9'
bed_list = []

index = 0
for pos in subset_df['Pos']:
    string = '{}'.format(scaffold)
    bef = int(pos) - 1
    snp = subset_df.iloc[index]['Proxy Variant']
    string += '\t{}\t{}\t{}\n'.format(bef, pos, snp)
    index += 1
    bed_list.append(string)

# repeat for table 11
raw2 = pd.read_csv('t11.csv', sep=',', header=0)
subset2 = raw2[raw2['Locus'] == 'IQCK']

# reset index counter
index = 0
for pos in subset2['Pos']:
    string = '{}'.format(scaffold)
    bef = int(pos) - 1
    snp = subset2.iloc[index]['rsID']
    string += '\t{}\t{}\t{}\n'.format(bef, pos, snp)
    index += 1
    bed_list.append(string)

# remove duplicate entries in bed_list
final_list = list(dict.fromkeys(bed_list))

# write each entry in bed_list to output file (.bed file)
for i in final_list:
    outFile.write(i)
