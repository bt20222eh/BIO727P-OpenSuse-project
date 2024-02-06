import csv
from collections import defaultdict, Counter

# Step 1: Read the input file and count the occurrences of each genotype for each SNP
snp_genotype_counts = defaultdict(Counter)
input_file_path = 'output.tsv'

with open(input_file_path, mode='r', newline='') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    for row in reader:
        snp_id = row['SNP_ID']
        genotype = row['GENOTYPE']
        snp_genotype_counts[snp_id][genotype] += 1

# Step 2: Calculate the frequency of each genotype for each SNP
snp_genotype_frequencies = defaultdict(dict)
for snp_id, genotype_counts in snp_genotype_counts.items():
    total_count = sum(genotype_counts.values())
    for genotype, count in genotype_counts.items():
        frequency = count / total_count
        snp_genotype_frequencies[snp_id][genotype] = frequency

# Step 3: Write the results to a new file
output_file_path = 'output_with_frequencies.tsv'
with open(input_file_path, mode='r', newline='') as infile, open(output_file_path, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = ['Sample_ID', 'SNP_ID', 'GENOTYPE', 'GenotypeFrequency']  # Define the fieldnames for the output
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    
    for row in reader:
        snp_id = row['SNP_ID']
        genotype = row['GENOTYPE']
        frequency = snp_genotype_frequencies[snp_id].get(genotype, 0)
        writer.writerow({
            'Sample_ID': row['Sample_ID'],
            'SNP_ID': snp_id,
            'GENOTYPE': genotype,
            'GenotypeFrequency': frequency
        })
