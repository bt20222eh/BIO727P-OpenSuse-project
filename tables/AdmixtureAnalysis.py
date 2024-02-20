# linux code to create .bed (binary PLINK), .bim (binary marker information file) and .fam (pedigree stub file) using PLINK:

# Download PLINK
wget http://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20201019.zip

# Unzip the downloaded file
unzip plink_linux_x86_64_20201019.zip

# Move the PLINK executable to a directory in your PATH (e.g., /usr/local/bin/)
sudo mv plink /usr/local/bin/

#create files from our filtered vcf
plink --vcf filtered_chr1.vcf.gz --make-bed --out filteredplinkfile --allow-extra-chr

#linux code for admixture to create .P and .Q files:
# Download ADMIXTURE
wget https://dalexander.github.io/admixture/binaries/admixture_linux-1.3.0.tar.gz

# Unpack the downloaded file
tar -zxvf admixture_linux-1.3.0.tar.gz

# Move the ADMIXTURE executable to a directory in your PATH (e.g., /usr/local/bin/)
sudo mv admixture_linux-1.3.0/admixture /usr/local/bin/

#run linux code for admixture for different K values to find a good value of K, which should exhibit a low cross-validation error compared to other K values:
#generates .P and .Q files as well as log files with the CV error

for K in 1 2 3 4 5 6 7 8; do admixture --cv hapmap3.bed $K | tee log${K}.out; done

#in this case the CV errors were found to be:
#CV error (K=1): 0.55740
#CV error (K=2): 0.51293
#CV error (K=3): 0.48937
#CV error (K=4): 0.48295
#CV error (K=5): 0.47878
#CV error (K=6): 0.47489
#CV error (K=7): 0.47451
#CV error (K=8): 0.47425
#so K=6 was chosen as gains in accuracy from then on were negligible


#python code to create tsv file from Q file after admixture:
import pandas as pd

# Specify the path to your .Q file
q_file_path = 'filteredplinkfile.6.Q'

# Read the .Q file into a Pandas DataFrame
admixture_data = pd.read_csv(q_file_path, sep='\s+', header=None)

# Specify the path for the output TSV file
output_tsv_path = 'output_admixture_results.tsv'

# Save the DataFrame to a TSV file
admixture_data.to_csv(output_tsv_path, sep='\t', index=False, header=False)

# Replace 'file1.tsv' and 'file2.tsv' with the actual file paths
file1_path = 'sample_pop.tsv'
file2_path = 'output_admixture_results.tsv'

# Read the first column from file1.tsv
column_to_add = pd.read_csv(file1_path, sep='\t', usecols=[0])

# Read the entire DataFrame from file2.tsv
df2 = pd.read_csv(file2_path, sep='\t')

# Concatenate the DataFrames
result_df = pd.concat([column_to_add, df2], axis=1)

# Save the result DataFrame to a new TSV file
result_df.to_csv('combined_file.tsv', sep='\t', index=False)

# Specify the path to your input TSV file
input_tsv_path = 'combined_file.tsv'

# Read the TSV file into a Pandas DataFrame
df = pd.read_csv(input_tsv_path, sep='\t')

# Rename columns from the 2nd column onwards
new_headers = [f'Ancestry {i}' for i in range(1, len(df.columns))]
df.columns = ['Sample'] + new_headers

# Specify the path for the output TSV file
output_tsv_path = 'AdmixtureAnalysis.tsv'

# Save the DataFrame to a new TSV file
df.to_csv(output_tsv_path, sep='\t', index=False)








