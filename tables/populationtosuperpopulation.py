import pandas as pd

# Load the dataset
file_path_population = 'Desktop/group_project_data_2024/population.tsv'
population_df = pd.read_csv(file_path_population, sep='\t', header=0)

# Define the mapping from population codes to super-populations
super_population_mapping = {
    'ACB': 'AFR', 'ASW': 'AFR', 'ESN': 'AFR', 'GWD': 'AFR', 'LWK': 'AFR', 'MSL': 'AFR', 'YRI': 'AFR',
    'CLM': 'AMR', 'MXL': 'AMR', 'PEL': 'AMR', 'PUR': 'AMR',
    'CDX': 'EAS', 'CHB': 'EAS', 'CHS': 'EAS', 'JPT': 'EAS', 'KHV': 'EAS',
    'CEU': 'EUR', 'FIN': 'EUR', 'GBR': 'EUR', 'IBS': 'EUR', 'TSI': 'EUR',
    'BEB': 'SAS', 'GIH': 'SAS', 'ITU': 'SAS', 'PJL': 'SAS', 'STU': 'SAS', 'SIB' :'EAS'
}

# Map population codes to super-populations, leaving 'SIB' or any other undefined codes blank
population_df['Super-population'] = population_df['population'].map(super_population_mapping)

# Verify the changes
print(population_df.head())
unique=population_df.drop_duplicates()

# Display the DataFrame after removing duplicates to verify
unique
# save the dataframe into a tsv file. 
unique.to_csv('Desktop/group_project_data_2024/updated_population.tsv', sep='\t', index=False)

