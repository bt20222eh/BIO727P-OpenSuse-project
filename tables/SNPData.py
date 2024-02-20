# Importing all the neccessary libraries
import requests
import csv 
def fetch_studies_for_snp(snp_id):
    """ fetches the mutations realating to Single Nucleotides polymorphisms ( SNPs) SNPIDs
    parameters : 
    - SNP_ID str : the ID of the snp to fetch the required data 
    returns : 
    - JSON respons containing the studies if successful , None otherwise. 
    """
    url = f'https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{snp_id}/studies'
    response = requests.get(url, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching studies for SNP {snp_id}: {response.status_code} - {response.text}')
        return None
        
# Defining a function to extract study information from the fetched studies data 
def extract_study_info(studies_data):
    """ Extracts study information from the studies data. 
    parameters : 
    - studies_data (dict) : the JSON data of studies related to a SNP.
    Returns : 
    - A list of dictionaries with 'diseaseTrait' keys and their corresponding values. 
    """
    study_details = []
    if not studies_data or '_embedded' not in studies_data or 'studies' not in studies_data['_embedded']:
        print('No study data found')
        return study_details
    
    for study in studies_data['_embedded']['studies']:
        study_info = {'diseaseTrait': study.get('diseaseTrait', {}).get('trait', 'Not specified')}
        study_details.append(study_info)
    
    return study_details

# Function to fetch gene information for a given SNP based on its chromosomal location
def fetch_gene_for_snp(chromosomal_location):
    """
    Fetches gene information for a given chromosomal location.
    Parameters:
    - chromosomal_location (str): The chromosomal location of the SNP.
    Returns:
    - A list of gene names if successful, None otherwise.
    """
    url = f'https://rest.ensembl.org/overlap/region/human/{chromosomal_location}?feature=gene'
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        data = response.json()
        genes = [gene['external_name'] for gene in data if gene.get('external_name')]
        return genes
    else:
        print(f'Error fetching gene for location {chromosomal_location}: {response.status_code} - {response.text}')
        return None

# Main function to process SNP data from an input file and output the results to SNPData.tsv
def process_snp_data(input_file_path, output_file_path):
    """
    Processes SNP data from an input file and writes the results to an output file.
    Parameters:
    - input_file_path (str): Path to the input file containing SNP data.
    - output_file_path (str): Path to the output file where results will be written.
    """
    # Read SNP IDs and their chromosomal locations from the input file
    snp_info = []
    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header row
        for row in reader:
            snp_id = row[0]  # Coloumn containing SNP_IDs  
            chromosomal_location = row[2]  # Column containing chromosomal locations
            snp_info.append((snp_id, chromosomal_location))
            
    # Writing the results from the above functions into an output file 
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['SNP_ID', 'DiseaseTrait', 'Genes'])

        for snp_id, position in snp_info:
            studies = fetch_studies_for_snp(snp_id)
            study_details = extract_study_info(studies)
            genes = fetch_gene_for_snp(position) if position else []
            
            for detail in study_details:
                writer.writerow([snp_id, detail['diseaseTrait'], ', '.join(genes)])
# Paths for the input and output files
input_file_path = 'SNPData.tsv'
output_file_path = 'output.tsv' 
# calling the main processing function: 
process_snp_data(input_file_path , output_file_path)


                
