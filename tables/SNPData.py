import requests

def fetch_studies_for_snp(snp_id):
    url = f'https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{snp_id}/studies'
    response = requests.get(url, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching studies for SNP {snp_id}: {response.status_code} - {response.text}')
        return None
def extract_study_info(studies_data):
    study_details = []
    if not studies_data or '_embedded' not in studies_data or 'studies' not in studies_data['_embedded']:
        print('No study data found')
        return study_details
    
    for study in studies_data['_embedded']['studies']:
        study_info = {
            'diseaseTrait': study.get('diseaseTrait', {}).get('trait', 'Not specified'),
        }
        study_details.append(study_info)
    
    return study_details
import csv

input_file_path = 'output.tsv'  # Change this to the path of your input file

snp_ids = []
with open(input_file_path, mode='r', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the header row
    for row in reader:
        snp_ids.append(row[1])  # Assuming SNP_ID is in the first column

output_file_path = 'snp_disease_traits.tsv'

with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    
    # Write the header
    writer.writerow(['SNP_ID', 'DiseaseTrait'])
    
    # Iterate over SNP IDs
    for snp_id in snp_ids:
        studies = fetch_studies_for_snp(snp_id)
        study_details = extract_study_info(studies)
        
        # Use a set to keep track of diseases we've already written for this SNP
        written_diseases = set()
        
        for detail in study_details:
            # Check if we've already written this disease for this SNP
            if detail['diseaseTrait'] not in written_diseases:
                writer.writerow([snp_id, detail['diseaseTrait']])
                written_diseases.add(detail['diseaseTrait'])

input_file_path = 'output_header.tsv'
import csv

input_file_path = 'output_header.tsv'
output_file_path = 'modified_output_header.tsv'

with open(input_file_path, mode='r', newline='') as infile, open(output_file_path, mode='w', newline='') as outfile:
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')
    
    # Copy the header
    header = next(reader)
    writer.writerow(header)
    
    # Iterate over the rows in the original file
    for row in reader:
        # Prepend '1:' to the position (assuming position is in the third column)
        row[2] = '1:' + row[2]
        
        # Write the modified row to the new file
        writer.writerow(row)
snp_info = []

with open(input_file_path, mode='r', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the header row
    for row in reader:
        snp_id = row[0]
        chromosomal_location = row[2]  # Assuming the location is in the third column
        snp_info.append((snp_id, chromosomal_location))
def fetch_gene_for_snp(chromosomal_location):
    url = f'https://rest.ensembl.org/overlap/region/human/{chromosomal_location}?feature=gene'
    headers = { 'Content-Type' : 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        genes = [gene['external_name'] for gene in data if gene.get('external_name')]
        return genes
    else:
        print(f'Error fetching gene for location {chromosomal_location}: {response.status_code} - {response.text}')
        return None
output_file_path = 'snp_disease_traits_genes.tsv'

with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    
    # Write the header
    writer.writerow(['SNP_ID', 'ChromosomalLocation', 'Genes'])
    
    chromosome_number = '1'  # Set the chromosome number here
for snp_id, position in snp_info:
    chromosomal_location = f'{chromosome_number}:{position}'
    genes = fetch_gene_for_snp(chromosomal_location)
