import requests

def fetch_studies_for_snp(snp_id):
    url = f'https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{snp_id}/studies'
    response = requests.get(url, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching studies for SNP {snp_id}: {response.status_code} - {response.text}')
        return {'_embedded': {'studies': []}}  # Return an empty structure
def extract_study_info(studies_data):
    disease_traits = set()
    if not studies_data or '_embedded' not in studies_data or 'studies' not in studies_data['_embedded']:
        print('No study data found')
        return disease_traits
    
    for study in studies_data['_embedded']['studies']:
        disease_trait = study.get('diseaseTrait', {}).get('trait', 'Not specified')
        disease_traits.add(disease_trait)
    
    return disease_traits
  input_file_path = 'output_header.tsv'  # Change this to the path of your input file

snp_ids = []
with open(input_file_path, mode='r', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the header row
    for row in reader:
        snp_ids.append(row[1])  # Assuming SNP_ID is in the first column
output_file_path = 'snp_disease_traits.tsv'  # Output file

with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    
    # Write the header
    writer.writerow(['SNP_ID', 'DiseaseTrait'])
    
    # Iterate over SNP IDs
    for snp_id in snp_ids:
        studies = fetch_studies_for_snp(snp_id)
        disease_traits = extract_study_info(studies)
        
        # Check if any disease traits were found
        if disease_traits:
            for trait in disease_traits:
                writer.writerow([snp_id, trait])
        else:
            # Write the SNP ID with a message indicating no clinical information
            writer.writerow([snp_id, 'No associated clinical information for this SNP'])
