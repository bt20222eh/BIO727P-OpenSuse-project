import pandas as pd
# import output data .tsv as dataframe
output_data=pd.read_csv('output.tsv', sep= '\t', header=None)
# Rename the header - columns
output_data.columns= ['sample_ID', 'SNP_ID', 'POS', 'REF', 'ALT', 'AN', 'AC', 'GT']
# Function to calculate genotype frequencies based on AN and AC
def calculate_genotype_frequency(an, ac, gt):
    if gt == '0/0' or gt == '0|0':
        return ac / (2 * an)
    elif gt == '0/1':
        return ac / an
    elif gt == '1/1':
        return ac / (2 * an)
    else:
        return None

    # Apply the function to calculate genotype frequencies and insert into a new column
    output_data['GT_frequency'] = output_data.apply(lambda row: calculate_genotype_frequency(row['AN'], row['AC'], row['GT']), axis=1)

    return output_data
# drop columns you don't need
complete_data= output_data.drop(['POS', 'REF', 'ALT', 'AN', 'AC'], axis=1)
# export the df as tsv file
file= complete_data.to_csv('complete_data.tsv', sep='\t')




