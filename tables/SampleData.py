# making tsv with only sample/snp id data
# Extract SNP ID and Sample ID - table neccessary to match every  SAMPLE_ID to the matching SNP_ID
output_df = pd.read_csv('output.tsv' , sep='\t')
snp_sample_df = output_df[['Sample_ID', 'SNP_ID']]

# Drop duplicates if necessary
snp_sample_df = snp_sample_df.drop_duplicates()

# Write to a TSV file
snp_sample_df.to_csv("SampleData.tsv", sep="\t", index=False)
