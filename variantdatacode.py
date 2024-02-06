import pandas as pd

# Define the filepath of the .tsv file
file_path = 'output.tsv'

# Read the .tsv file into a DataFrame
df = pd.read_csv(file_path, sep='\t', header=None)

df['AF'] = df[6] / df[5]

df = df.drop([2, 3, 4, 5, 6, 7], axis=1)

new_columns = ['Sample_ID', 'SNP_ID', 'AF']
df.columns = new_columns

#give sample output to test
print(df.head())
