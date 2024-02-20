# making tsv with only sample/snp id data
# Extract SNP ID and Sample ID
snp_sample_df = variant_data_df[['Sample_ID', 'SNP_ID']]

# Drop duplicates if necessary
snp_sample_df = snp_sample_df.drop_duplicates()

# Write to a TSV file
snp_sample_df.to_csv("snp_sample_ids.tsv", sep="\t", index=False)
