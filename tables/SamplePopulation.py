def calculate_genotype_frequencies(input_file):
    genotype_counts = {}
    sample_counts = {}

    with open(input_file, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split('\t')
            sample_id = parts[0]
            genotype = parts[-1]

            if sample_id not in genotype_counts:
                genotype_counts[sample_id] = {'00': 0, '01': 0, '11': 0}
                sample_counts[sample_id] = 0

            if '/' in genotype:
                if genotype == '0/0':
                    genotype_counts[sample_id]['00'] += 1
                elif genotype == '0/1':
                    genotype_counts[sample_id]['01'] += 1
                elif genotype == '1/1':
                    genotype_counts[sample_id]['11'] += 1
            elif '|' in genotype:
                alleles = genotype.split('|')
                if alleles[0] == '0' and alleles[1] == '0':
                    genotype_counts[sample_id]['00'] += 1
                elif alleles[0] == '0' and alleles[1] == '1':
                    genotype_counts[sample_id]['01'] += 1
                elif alleles[0] == '1' and alleles[1] == '1':
                    genotype_counts[sample_id]['11'] += 1

            sample_counts[sample_id] += 1

    genotype_frequencies = {}
    for sample_id, counts in genotype_counts.items():
        total_samples = sample_counts[sample_id]
        genotype_frequencies[sample_id] = {
            'GTFreq_00': counts.get('00', 0) / total_samples,
            'GTFreq_01': counts.get('01', 0) / total_samples,
            'GTFreq_11': counts.get('11', 0) / total_samples
        }

    return genotype_frequencies

def write_genotype_frequencies(genotype_frequencies, output_file):
    with open(output_file, 'w') as file:
        file.write("SampleID\tGTFreq_00\tGTFreq_01\tGTFreq_11\n")
        for sample_id, frequencies in genotype_frequencies.items():
            # Write sample ID and genotype frequencies
            file.write(f"{sample_id}\t{frequencies['GTFreq_00']}\t{frequencies['GTFreq_01']}\t{frequencies['GTFreq_11']}\n")

# Input and output files
input_file = "output.tsv"
output_file = "sample_genotype_frequencies.tsv"

# Calculate genotype frequencies
genotype_frequencies = calculate_genotype_frequencies(input_file)

# Write genotype frequencies to a new file
write_genotype_frequencies(genotype_frequencies, output_file)

print(f"Genotype frequencies have been written to {output_file}.")

# Function to calculate allele frequencies from genotype frequencies
def calculate_allele_frequencies(gt_freqs):
    allele_freqs = {}
    for sample_id, frequencies in gt_freqs.items():
        ref_freq = frequencies['GTFreq_00'] + (0.5 * frequencies['GTFreq_01'])
        alt_freq = 1 - ref_freq
        allele_freqs[sample_id] = {'REF_Freq': ref_freq, 'ALT_Freq': alt_freq}
    return allele_freqs

# Read genotype frequencies from the file
genotype_frequencies_file = "sample_genotype_frequencies.tsv"
genotype_frequencies = {}

with open(genotype_frequencies_file, 'r') as file:
    lines = file.readlines()
    headers = lines[0].strip().split('\t')
    for line in lines[1:]:
        data = line.strip().split('\t')
        sample_id = data[0]
        frequencies = {header: float(freq) for header, freq in zip(headers[1:], data[1:])}
        genotype_frequencies[sample_id] = frequencies

# Calculate allele frequencies
allele_frequencies = calculate_allele_frequencies(genotype_frequencies)

# Write combined data to a new file
combined_file = "combined_frequencies.tsv"
with open(combined_file, 'w') as file:
    # Write headers
    file.write("Sample_ID\tGTFreq_00\tGTFreq_01\tGTFreq_11\tREF_Freq\tALT_Freq\n")
    
    # Write data
    for sample_id, gt_frequencies in genotype_frequencies.items():
        allele_freqs = allele_frequencies[sample_id]
      file.write(f"{sample_id}\t{gt_frequencies['GTFreq_00']}\t{gt_frequencies['GTFreq_01']}\t{gt_frequencies['GTFreq_11']}\t{allele_freqs['REF_Freq']}\t{allele_freqs['ALT_Freq']}\n")

print(f"Combined data has been written to {combined_file}.")
