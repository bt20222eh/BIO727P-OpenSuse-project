def calculate_genotype_frequencies(input_file): 
    """ this function calculates the genotype frequencies from SNP data, and makes sure it 
    counts the genotype from all samples and ensures that it collects them in both / and | format
    Args: input_file str : the path to the input tsv file containing SNP data 
    Returns : 
    dict : A dictionary mapping each sample
    """
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
# count the frequency for the three different genotypes taking to account SIB and all the other populations. 
            if '/' in genotype:
                if genotype in ['0/0', '0|0']:
                    genotype_counts[sample_id]['00'] += 1
                elif genotype in ['0/1', '1/0', '0|1', '1|0']:
                    genotype_counts[sample_id]['01'] += 1
                elif genotype in ['1/1', '1|1']:
                    genotype_counts[sample_id]['11'] += 1
            elif '|' in genotype:
                if genotype in ['0/0', '0|0']:
                    genotype_counts[sample_id]['00'] += 1
                elif genotype in ['0/1', '1/0', '0|1', '1|0']:
                    genotype_counts[sample_id]['01'] += 1
                elif genotype in ['1/1', '1|1']:
                    genotype_counts[sample_id]['11'] += 1

            sample_counts[sample_id] += 1
# calculate the frequencies for each genotype per sample. 
    genotype_frequencies = {}
    for sample_id, counts in genotype_counts.items():
        total_samples = sample_counts[sample_id]
        genotype_frequencies[sample_id] = {
            'GTFreq_00': counts.get('00', 0) / total_samples,
            'GTFreq_01': counts.get('01', 0) / total_samples,
            'GTFreq_11': counts.get('11', 0) / total_samples
        }

    return genotype_frequencies

# Function to write the genotype frequencies to a TSV file 
def write_genotype_frequencies(genotype_frequencies, output_file):
    """ Writes the calcualted genotype frequencies to an output TSV file.
    Args :
    genotype_frequencies ( dict ) :" A dictionary of genotype frequencies by sample ID
    output_file ( str) : The path to the output TSV file . """
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
    """
    Calculates the frequencies of reference and alternate alleles based on genotype frequencies.

    Args:
    genotype_frequencies (dict): A dictionary of genotype frequencies by sample ID.

    Returns:
    dict: A dictionary mapping each sample ID to its allele frequencies.
    """
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
# calculate genotype frequencies 
genotype_frequencies = calculate_genotype_frequencies(input_file)
# Write combined data to a new file
combined_file = "combined_frequencies.tsv"
with open(combined_file, 'w') as file:
    # Write headers
    file.write("Sample_ID\tGTFreq_00\tGTFreq_01\tGTFreq_11\tREF_Freq\tALT_Freq\n")
    
    # Write data
    for sample_id, gt_frequencies in genotype_frequencies.items():
        allele_freqs = allele_frequencies[sample_id]
      file.write(f"{sample_id}\t{gt_frequencies['GTFreq_00']}\t{gt_frequencies['GTFreq_01']}\t{gt_frequencies['GTFreq_11']}\t{allele_freqs['REF_Freq']}\t{allele_freqs['ALT_Freq']}\n")

# All the files required for the functions to work 
input_file = ('output.tsv')
genotype_freq_file = ('updated_population.tsv')
combined_freq_file = ('combined_frequencies.tsv')
print(f"Combined data has been written to {combined_file}.")

import pandas as pd

# load the relevant TSV files
combined_freq_file_path = 'combined_frequencies.tsv'
sample_pop_file_path = 'sample_pop.tsv'
population_superpopulation_file_path = 'population_superpopulation.tsv'

# read the files
combined_freq_df = pd.read_csv(combined_freq_file_path, sep='\t')
sample_pop_df = pd.read_csv(sample_pop_file_path, sep='\t')
popultation_superpopulation_df = pd.read_csv(population_superpopulation_file_path, sep='\t')

# display the first few rows of each DataFrame to understand their structure
combined_freq_df.head(), sample_pop_df.head(), population_superpopulation_df.head()
# reorder the columns 
final_df_reordered = final_df[['id', 'Population', 'Super_population', 'GTFreq_00', 'GTFreq_01', 'GTFreq_11', 'REF_Freq', 'ALT_Freq', 'REF_Freq_avg', 'ALT_Freq_avg']]

# save the reordered DataFrame to a new TSV file
output_file_path_reordered = 'SamplePopulation.tsv'
final_df_reordered.to_csv(output_file_path_reordered, sep='\t', index=False)

# provide the path for download
output_file_path_reordered






