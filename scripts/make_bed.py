# make_bed.py

import pandas as pd

raw_df = pd.read_csv('t9.csv', sep=',', header=2)
subset_df = raw_df[raw_df['LOCUS'] == 'IQCK']

outFileName = 'IQCK_variants.BED'
outFile = open(outFileName, 'w+')

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


raw2 = pd.read_csv('t11.csv', sep=',', header=0)
subset2 = raw2[raw2['Locus'] == 'IQCK']

index = 0
for pos in subset2['Pos']:
    string = '{}'.format(scaffold)
    bef = int(pos) - 1
    snp = subset2.iloc[index]['rsID']
    string += '\t{}\t{}\t{}\n'.format(bef, pos, snp)
    index += 1
    bed_list.append(string)


final_list = list(dict.fromkeys(bed_list))

for i in final_list:
    outFile.write(i)
