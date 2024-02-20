import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the cleaned data obtained from BCFTOOLs (removal of all data containing any missing fields )
data = pd.read_csv('output.tsv', sep='\t', header=0)

# Drop unnecessary columns
data.drop(['REF', 'ALT', 'AC', 'AN', 'POS'], axis=1, inplace=True)

# Convert Genotypes to Numerical Values
def genotype_to_numeric(genotype):
    return genotype.count('1')

data['NumericGenotype'] = data['GENOTYPE'].apply(genotype_to_numeric)

# Create Matrix for PCA
pca_input = data.pivot_table(index='Sample_ID', columns='SNP_ID', values='NumericGenotype', fill_value=0)

# Normalize the Data
scaler = StandardScaler()
pca_input_scaled = scaler.fit_transform(pca_input)

# Perform PCA
pca = PCA(n_components=2)  # Adjust n_components based on your needs , here we use 2 componenets as they captue the most variance 
pca_result = pca.fit_transform(pca_input_scaled)

# Convert PCA result into a DataFrame for easier handling and retrieval 
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])

print(pca_df)
pca_df['SampleID'] = pop_codes_df['SampleID'].values[:len(pca_df)]

# Merge PCA results with population codes using the newly added 'SampleID' - easier for SQL query upon user requests 
pca_pop_df = pca_df.merge(pop_codes_df, on='SampleID')

# Define a list of 27 distinct colors - so that each population shows up as as different colour on the PCA plot for easier analysis 
colors = [
    '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',
    '#00FFFF', '#800000', '#008000', '#000080', '#FFA500',
    '#FFFF80', '#FF80FF', '#80FFFF', '#800080', '#808000',
    '#008080', '#FF4500', '#00FF80', '#0000A0', '#FFD700',
    '#FF69B4', '#00FA9A', '#9400D3', '#FF6347', '#00FF7F',
    '#1E90FF', '#FFC0CB'
]

# Plot the PCA results color-coded by population
fig, ax = plt.subplots(figsize=(12, 10))

groups = pca_pop_df.groupby('Population')
for idx, (name, group) in enumerate(groups):
    ax.plot(group['PC1'], group['PC2'], marker='o', linestyle='', ms=6, label=name, color=colors[idx])

# Adjust legend to be outside the plot to the right
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('PCA by Population')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.grid(True)
plt.tight_layout() # Adjust the layout to make room for the legend

plt.show()

# now to store the dataframe in the databse with only the ccrrect coloumns neccessary to reduce data redundancy 
pca_df = pca_df[['SampleID', 'PC1', 'PC2']]
# save the pca_df as a tsv to easily put in the database as a table 
pca_df.to_csv('pca_modified.tsv', sep='\t', index=False)


