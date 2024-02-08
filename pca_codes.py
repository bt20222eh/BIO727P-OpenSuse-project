import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load your data
data = pd.read_csv('output.tsv', sep='\t', header=None)
data.columns = ['Individual', 'SNP_ID', 'Position', 'Ref', 'Alt', 'Value1', 'Value2', 'Genotype']

# Drop unnecessary columns
data.drop(['Ref', 'Alt', 'Value1', 'Value2', 'Position'], axis=1, inplace=True)

# Convert Genotypes to Numerical Values
def genotype_to_numeric(genotype):
    return genotype.count('1')

data['NumericGenotype'] = data['Genotype'].apply(genotype_to_numeric)

# Create Matrix for PCA
pca_input = data.pivot_table(index='Individual', columns='SNP_ID', values='NumericGenotype', fill_value=0)

# Normalize the Data
scaler = StandardScaler()
pca_input_scaled = scaler.fit_transform(pca_input)

# Perform PCA
pca = PCA(n_components=2)  # Adjust n_components based on your needs
pca_result = pca.fit_transform(pca_input_scaled)

# Convert PCA result into a DataFrame for easier handling
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])

print(pca_df)

# colour coding 
import matplotlib.pyplot as plt

# Assuming the full PCA results are already in pca_df as described earlier
# Add 'SampleID' from the full 'pop_codes_df' to the 'pca_df'
pca_df['SampleID'] = pop_codes_df['SampleID'].values[:len(pca_df)]

# Merge PCA results with population codes using the newly added 'SampleID'
pca_pop_df = pca_df.merge(pop_codes_df, on='SampleID')

# Define a list of 27 distinct colors
colors = [
    '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',
    '#00FFFF', '#800000', '#008000', '#000080', '#FFA500',
    '#FFFF80', '#FF80FF', '#80FFFF', '#800080', '#808000',
    '#008080', '#FF4500', '#00FF80', '#0000A0', '#FFD700',
    '#FF69B4', '#00FA9A', '#9400D3', '#FF6347', '#00FF7F',
    '#1E90FF', '#FFC0CB'
]



# Now let's plot the PCA results color-coded by population
fig, ax = plt.subplots(figsize=(12, 10))

groups = pca_pop_df.groupby('Population')
for idx, (name, group) in enumerate(groups):
    ax.plot(group['PC1'], group['PC2'], marker='o', linestyle='', ms=6, label=name, color=colors[idx])

ax.legend()
plt.title('PCA by Population')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.grid(True)
plt.show()

pop_codes_df = pd.read_csv('sample_pop.csv', '\t')
pop_codes_df.rename(columns={'id': 'SampleID', 'population': 'Population'}, inplace=True)
super_pop_codes_df = pd.read_csv('updated_population.tsv', sep='\t')

# Assuming pca_df, pop_codes_df, and super_pop_codes_df are already defined as described

# First, merge pca_df with pop_codes_df to associate each PCA result with its population
combined_df = pca_df.merge(pop_codes_df, left_on='SampleID', right_on='SampleID')

# Then, rename the column 'population' in super_pop_codes_df to 'Population' for a consistent merge
super_pop_codes_df.rename(columns={'population': 'Population'}, inplace=True)

# Now, merge the combined_df with super_pop_codes_df to include the super-population
final_df = combined_df.merge(super_pop_codes_df, on='Population')

# Finally, rename the columns to match the structure of the table in your image
final_df.rename(columns={'PC1': 'pc1', 'PC2': 'pc2', 'Population': 'population', 'Super-population': 'sub_population'}, inplace=True)

# Reorder the columns to match the desired output
final_df = final_df[['SampleID', 'population', 'sub_population', 'pc1', 'pc2']]

# Display the final DataFrame
print(final_df)

# Save the DataFrame to a TSV file
final_df.to_csv('pca.tsv', sep='\t', index=False)





